from fastapi import FastAPI, Depends, HTTPException
from typing import List
from . import models, schemas, crud, database, logger
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/elements/")
def create(payload: schemas.Payload, db: Session = Depends(get_db)):
    crud.create_entries(db, payload)
    return {"message": "Entries processed and stored"}

@app.get("/api/elements/", response_model=List[schemas.EntryResponse])
def read_all(db: Session = Depends(get_db)):
    return crud.get_entries(db)

@app.get("/api/elements/{entry_id}/", response_model=schemas.EntryResponse)
def read(entry_id: str, db: Session = Depends(get_db)):
    entry = crud.get_entry(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@app.put("/api/elements/{entry_id}/")
def update(entry_id: str, device_name: str, db: Session = Depends(get_db)):
    entry = crud.update_entry(db, entry_id, device_name)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"message": "Entry updated"}

@app.delete("/api/elements/{entry_id}/")
def delete(entry_id: str, db: Session = Depends(get_db)):
    crud.delete_entry(db, entry_id)
    return {"message": "Entry deleted"}