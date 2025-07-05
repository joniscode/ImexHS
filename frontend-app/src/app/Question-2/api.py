from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from file_processor import FileProcessor
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

processor = FileProcessor(base_path="data", log_file="logs/processor.log")

class FolderRequest(BaseModel):
    folder_name: str
    details: bool = False

class CsvRequest(BaseModel):
    filename: str
    summary: bool = False

class DicomRequest(BaseModel):
    filename: str
    tags: Optional[List[List[int]]] = None  # Acepta [[16, 16], [8, 96]]
    extract_image: bool = False

@app.post("/list-folder")
def list_folder(data: FolderRequest):
    return processor.list_folder_contents(data.folder_name, data.details)

@app.post("/read-csv")
def read_csv(data: CsvRequest):
    return processor.read_csv(data.filename, summary=data.summary)

@app.post("/read-dicom")
def read_dicom(data: DicomRequest):
    return processor.read_dicom(
        data.filename,
        tags=[(int(tag[0]), int(tag[1])) for tag in data.tags] if data.tags else None,
        extract_image=data.extract_image
    )
