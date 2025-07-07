from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from fastapi import FastAPI, HTTPException, Path as FPath, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, RootModel, field_validator
from sqlalchemy import (
    Float, Integer, String, DateTime, ForeignKey,
    create_engine, select, and_
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker
)
import logging


# CONFIGURACIÓN GENERAL 

APP_NAME = "Medical Results API"
DB_FILE  = Path("./data/medical_data.db")
LOG_DIR  = Path("./logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
DB_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "medical_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(title=APP_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True,
)

# BASE DE DATOS  
DATABASE_URL = f"sqlite:///{DB_FILE.as_posix()}"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)
SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

class Device(Base):
    __tablename__ = "devices"

    id   : Mapped[int]  = mapped_column(Integer, primary_key=True)
    name : Mapped[str]  = mapped_column(String, unique=True, nullable=False)
    elements: Mapped[List["Element"]] = relationship(back_populates="device", cascade="all, delete")

class Element(Base):
    __tablename__ = "elements"

    id          : Mapped[str]  = mapped_column(String, primary_key=True)
    device_id   : Mapped[int]  = mapped_column(ForeignKey("devices.id"))
    avg_before  : Mapped[float] = mapped_column(Float)
    avg_after   : Mapped[float] = mapped_column(Float)
    data_size   : Mapped[int]   = mapped_column(Integer)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    device: Mapped[Device] = relationship(back_populates="elements")

Base.metadata.create_all(engine)

# Pydantic Schemas 
class ElementInput(BaseModel):
    id: str
    data: List[str]
    deviceName: str

    @field_validator("data")
    @classmethod
    def only_numbers(cls, v: List[str]):
        for row in v:
            if any(not tok.isdigit() for tok in row.split()):
                raise ValueError("'data' contiene valores no numéricos")
        return v

class PayloadInput(RootModel[Dict[str, ElementInput]]):
    pass

class ElementResponse(BaseModel):
    id: str
    device_name: str
    avg_before: float
    avg_after: float
    data_size: int
    created_date: datetime
    updated_date: datetime

class ElementUpdate(BaseModel):
    device_name: Optional[str] = None
    new_id     : Optional[str] = None

# Helpers 

def calc_stats(rows: List[str]) -> Tuple[float, float, int]:
    nums = [int(tok) for row in rows for tok in row.split()]
    if not nums:
        raise ValueError("data vacío")
    max_val = max(nums)
    avg_before = sum(nums) / len(nums)
    normalized = [x / max_val for x in nums]
    avg_after = sum(normalized) / len(normalized)
    return avg_before, avg_after, len(nums)


# Endpoints (UPSERT)
@app.post("/api/elements/", response_model=list[ElementResponse])
def create_or_update_elements(payload: PayloadInput):
    responses: list[ElementResponse] = []
    with SessionLocal() as db:
        for elem in payload.root.values():
            try:
                avg_b, avg_a, size = calc_stats(elem.data)

                # get or create device
                device = db.scalar(select(Device).where(Device.name == elem.deviceName))
                if not device:
                    device = Device(name=elem.deviceName)
                    db.add(device)
                    db.flush()  # obtiene device.id

                # UPSERT --------
                record = db.get(Element, elem.id)
                if record:
                    record.device_id  = device.id
                    record.avg_before = avg_b
                    record.avg_after  = avg_a
                    record.data_size  = size
                    record.updated_date = datetime.utcnow()
                else:
                    record = Element(
                        id=elem.id,
                        device_id=device.id,
                        avg_before=avg_b,
                        avg_after=avg_a,
                        data_size=size,
                    )
                    db.add(record)

                db.commit(); db.refresh(record)

                responses.append(ElementResponse(
                    id=record.id,
                    device_name=device.name,
                    avg_before=record.avg_before,
                    avg_after=record.avg_after,
                    data_size=record.data_size,
                    created_date=record.created_date,
                    updated_date=record.updated_date,
                ))

            except Exception as exc:
                db.rollback()
                logging.error(f"Error en {elem.id}: {exc}")
                raise HTTPException(status_code=400, detail=f"Error en {elem.id}: {exc}")

    return responses

# ---------------- GET list --------
@app.get("/api/elements/", response_model=list[ElementResponse])
def list_elements(
    avg_before_min: float = Query(0, alias="avg_before_min"),
    avg_before_max: float = Query(1e9, alias="avg_before_max")
):
    stmt = select(Element).where(
        and_(Element.avg_before >= avg_before_min, Element.avg_before <= avg_before_max)
    )
    with SessionLocal() as db:
        rows = db.scalars(stmt).all()
        return [ElementResponse(
            id=r.id,
            device_name=r.device.name,
            avg_before=r.avg_before,
            avg_after=r.avg_after,
            data_size=r.data_size,
            created_date=r.created_date,
            updated_date=r.updated_date,
        ) for r in rows]

# ---------------- GET single -----
@app.get("/api/elements/{element_id}", response_model=ElementResponse)
def get_element(element_id: str = FPath(...)):
    with SessionLocal() as db:
        r = db.get(Element, element_id)
        if not r:
            raise HTTPException(status_code=404, detail="Elemento no encontrado")
        return ElementResponse(
            id=r.id, device_name=r.device.name,
            avg_before=r.avg_before, avg_after=r.avg_after,
            data_size=r.data_size, created_date=r.created_date,
            updated_date=r.updated_date,
        )

# ---------------- PUT / PATCH -----
@app.put("/api/elements/{element_id}")
def update_element(element_id: str, payload: ElementUpdate):
    with SessionLocal() as db:
        r = db.get(Element, element_id)
        if not r:
            raise HTTPException(status_code=404, detail="Elemento no encontrado")

        if payload.device_name:
            dev = db.scalar(select(Device).where(Device.name == payload.device_name))
            if not dev:
                dev = Device(name=payload.device_name); db.add(dev); db.flush()
            r.device_id = dev.id

        if payload.new_id:
            if db.get(Element, payload.new_id):
                raise HTTPException(status_code=400, detail="ID ya existe")
            r.id = payload.new_id

        db.commit()
        return {"message": "Elemento actualizado"}

# ---------------- DELETE ---
@app.delete("/api/elements/{element_id}")
def delete_element(element_id: str):
    with SessionLocal() as db:
        r = db.get
