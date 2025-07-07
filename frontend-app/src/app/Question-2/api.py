# Question-2/api.py
# ------------------------------------------------------------
from pathlib import Path
from typing import List, Optional, Tuple

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, FileResponse
from pydantic import BaseModel

from file_processor import FileProcessor   # tu clase

# ─── Configuración ───────────────────────────────────────────
BASE_PATH   = Path(__file__).parent / "data"     # ./Question-2/data
LOG_FILE    = Path(__file__).parent / "logs/processor.log"
processor   = FileProcessor(str(BASE_PATH), str(LOG_FILE))

app = FastAPI(title="File-Processor API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# ─── Modelos Pydantic usados por los endpoints ───────────────
class FolderReq(BaseModel):
    folder_name: str
    details: bool = False

class CsvReq(BaseModel):
    filename: str
    summary: bool = False
    report_path: Optional[str] = None

class DicomReq(BaseModel):
    filename: str
    tags: Optional[List[Tuple[int, int]]] = None
    extract_image: bool = False

# ─── Endpoints GET simples (listas) ──────────────────────────
@app.get("/list-dicoms", response_model=List[str])
def list_dicoms():
    return processor.list_dicom_files()

@app.get("/list-csvs",   response_model=List[str])
def list_csvs():
    return processor.list_csv_files()

# ─── Endpoints POST que devuelven texto plano ────────────────
@app.post("/list-folder", response_class=PlainTextResponse)
def list_folder(body: FolderReq):
    return processor.list_folder_contents(body.folder_name, body.details)

@app.post("/read-csv", response_class=PlainTextResponse)
def read_csv(body: CsvReq):
    return processor.read_csv(body.filename, body.report_path, body.summary)

@app.post("/read-dicom", response_class=PlainTextResponse)
def read_dicom(body: DicomReq):
    txt = processor.read_dicom(body.filename, body.tags, body.extract_image)
    # Si extrajo imagen, exponla como archivo estático:
    if body.extract_image:
        img_name = body.filename.replace(".dcm", ".png")
        img_path = Path("output") / img_name
        if img_path.exists():
            # FastAPI servirá /output/<png> como archivo
            app.mount("/output", StaticFiles(directory="output"), name="output")
    return txt

# ─── Descarga del reporte CSV generado por read_csv() ────────
@app.get("/reports/{file_name}", response_class=FileResponse)
def download_report(file_name: str):
    file_path = Path("reports") / file_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return FileResponse(file_path, media_type="text/plain", filename=file_name)
