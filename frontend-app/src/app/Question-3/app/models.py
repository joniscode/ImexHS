from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Device(Base):
    __tablename__ = 'devices'
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)

    results = relationship("Result", back_populates="device")

class Result(Base):
    __tablename__ = 'results'
    id = Column(String, primary_key=True, index=True)
    device_id = Column(String, ForeignKey('devices.id'))
    avg_before = Column(Float)
    avg_after = Column(Float)
    data_size = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    device = relationship("Device", back_populates="results")
