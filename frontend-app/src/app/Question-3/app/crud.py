from sqlalchemy.orm import Session
from . import models, schemas, utils
from datetime import datetime

def create_entries(db: Session, payload: schemas.Payload):
    for key, entry in payload.__root__.items():
        numbers = utils.parse_data(entry.data)
        norm_numbers = utils.normalize_data(numbers)
        avg_before = sum(numbers) / len(numbers)
        avg_after = sum(norm_numbers) / len(norm_numbers)

        device = db.query(models.Device).filter(models.Device.id == entry.id).first()
        if not device:
            device = models.Device(id=entry.id, device_name=entry.deviceName)
            db.add(device)
            db.flush()

        db_entry = models.Result(
            id=entry.id,
            device_id=device.id,
            avg_before=avg_before,
            avg_after=avg_after,
            data_size=len(numbers),
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )
        db.merge(db_entry)
    db.commit()


def get_entries(db: Session):
    return db.query(models.Result).all()


def get_entry(db: Session, entry_id: str):
    return db.query(models.Result).filter(models.Result.id == entry_id).first()


def update_entry(db: Session, entry_id: str, new_name: str):
    entry = db.query(models.Result).filter(models.Result.id == entry_id).first()
    if entry:
        entry.device.device_name = new_name
        db.commit()
    return entry


def delete_entry(db: Session, entry_id: str):
    entry = db.query(models.Result).filter(models.Result.id == entry_id).first()
    if entry:
        db.delete(entry)
        db.commit()