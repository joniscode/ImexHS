from pydantic import BaseModel
from typing import List

class ResultData(BaseModel):
    id: str
    data: List[str]
    deviceName: str

class ResultIn(BaseModel):
    __root__: dict[str, ResultData]
