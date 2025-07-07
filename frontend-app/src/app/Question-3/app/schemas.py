from typing import List, Dict
from pydantic import BaseModel, BaseModel

class Element(BaseModel):
    id: str
    data: List[str]
    deviceName: str

class Payload(BaseModel[Dict[str, Element]]):
    pass

class EntryResponse(BaseModel):
    id: str
    device_id: str
    avg_before: float
    avg_after: float
    data_size: int
    created_date: str
    updated_date: str

    class Config:
        orm_mode = True