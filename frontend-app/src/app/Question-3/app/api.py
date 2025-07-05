from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ResultIn
from database import SessionLocal, engine
from models import Base
from crud import process_and_store_result

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/elements/")
def create_elements(payload: ResultIn, db: Session = Depends(get_db)):
    for key, data in payload.__root__.items():
        try:
            process_and_store_result(db, data.id, data.data, data.deviceName)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error procesando {key}: {str(e)}")
    return {"message": "✅ Datos procesados correctamente"}
