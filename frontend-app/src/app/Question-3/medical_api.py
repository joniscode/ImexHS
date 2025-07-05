from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import logging

# --- CONFIGURACIÓN INICIAL ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, filename="logs/medical_api.log", format='%(asctime)s - %(message)s')

# --- DATABASE ---
DATABASE_URL = "sqlite:///./medical_data.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODELOS SQLALCHEMY ---
class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    elements = relationship("Element", back_populates="device")

class Element(Base):
    __tablename__ = "elements"
    id = Column(String, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    avg_before = Column(Float)
    avg_after = Column(Float)
    data_size = Column(Integer)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    device = relationship("Device", back_populates="elements")

Base.metadata.create_all(bind=engine)

# --- Pydantic SCHEMAS ---
class ElementInput(BaseModel):
    id: str
    data: List[str]
    deviceName: str

class PayloadInput(BaseModel):
    __root__: Dict[str, ElementInput]

class ElementResponse(BaseModel):
    id: str
    device_name: str
    avg_before: float
    avg_after: float
    data_size: int
    created_date: datetime
    updated_date: datetime

# --- FUNCIONES AUXILIARES ---
def normalize_and_average(data_strs: List[str]) -> (float, float):
    flat_data = [int(n) for row in data_strs for n in row.split() if n.isdigit()]
    if not flat_data:
        raise ValueError("No se encontraron datos válidos.")
    avg_before = sum(flat_data) / len(flat_data)
    max_val = max(flat_data)
    normalized = [x / max_val for x in flat_data]
    avg_after = sum(normalized) / len(normalized)
    return avg_before, avg_after

# --- ENDPOINTS ---
@app.post("/api/elements/", response_model=List[ElementResponse])
def create_elements(payload: PayloadInput):
    db = SessionLocal()
    responses = []
    for _, element in payload.__root__.items():
        try:
            avg_before, avg_after = normalize_and_average(element.data)
            
            # Verificar o crear dispositivo
            device = db.query(Device).filter_by(name=element.deviceName).first()
            if not device:
                device = Device(name=element.deviceName)
                db.add(device)
                db.commit()
                db.refresh(device)

            # Crear elemento
            el = Element(
                id=element.id,
                device_id=device.id,
                avg_before=avg_before,
                avg_after=avg_after,
                data_size=len(element.data),
            )
            db.add(el)
            db.commit()
            db.refresh(el)

            responses.append(ElementResponse(
                id=el.id,
                device_name=device.name,
                avg_before=el.avg_before,
                avg_after=el.avg_after,
                data_size=el.data_size,
                created_date=el.created_date,
                updated_date=el.updated_date
            ))
        except Exception as e:
            db.rollback()
            logging.error(f"Error al procesar elemento {element.id}: {e}")
            raise HTTPException(status_code=400, detail=f"Error en elemento {element.id}: {e}")
    return responses

@app.get("/api/elements/", response_model=List[ElementResponse])
def get_all_elements():
    db = SessionLocal()
    elements = db.query(Element).all()
    return [
        ElementResponse(
            id=el.id,
            device_name=el.device.name,
            avg_before=el.avg_before,
            avg_after=el.avg_after,
            data_size=el.data_size,
            created_date=el.created_date,
            updated_date=el.updated_date
        ) for el in elements
    ]

@app.get("/api/elements/{element_id}", response_model=ElementResponse)
def get_element_by_id(element_id: str):
    db = SessionLocal()
    el = db.query(Element).filter_by(id=element_id).first()
    if not el:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    return ElementResponse(
        id=el.id,
        device_name=el.device.name,
        avg_before=el.avg_before,
        avg_after=el.avg_after,
        data_size=el.data_size,
        created_date=el.created_date,
        updated_date=el.updated_date
    )

@app.put("/api/elements/{element_id}")
def update_element(element_id: str, new_data: Dict[str, str]):
    db = SessionLocal()
    el = db.query(Element).filter_by(id=element_id).first()
    if not el:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    
    if "device_name" in new_data:
        device = db.query(Device).filter_by(name=new_data["device_name"]).first()
        if not device:
            device = Device(name=new_data["device_name"])
            db.add(device)
            db.commit()
            db.refresh(device)
        el.device_id = device.id

    if "id" in new_data:
        el.id = new_data["id"]

    db.commit()
    return {"message": "Elemento actualizado correctamente"}

@app.delete("/api/elements/{element_id}")
def delete_element(element_id: str):
    db = SessionLocal()
    el = db.query(Element).filter_by(id=element_id).first()
    if not el:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    db.delete(el)
    db.commit()
    return {"message": f"Elemento {element_id} eliminado correctamente"}
