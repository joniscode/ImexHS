# Ejercicio 2: Procesamiento de Archivos
Este módulo permite listar carpetas, leer CSV y analizar archivos DICOM usando Angular + Python.

# 1. Crear entorno virtual (solo una vez)
python -m venv venv

# 2. 🚀 Tecnologías utilizadas

- **Frontend:** Angular 17 + Vite + SCSS
- **Backend:** FastAPI + Python 3.12
- **Otros:** pydicom, Pillow, NumPy, CORS, logging


# 3. Instalar dependencias dentro del entorno
pip install fastapi uvicorn pydicom numpy pillow

    ## Luego podrás correr el backend con:

    bash
    Copiar
    Editar
    uvicorn api:app --reload

# 4.📦 Estructura del proyecto

Question-2/
├── data/ # Archivos de entrada (CSV, DICOM)
│ ├── sample-02-csv.csv
│ ├── sample-02-dicom.dcm
├── venv/ # Archivos Necesarios
├── logs/ # Registro de errores
│ └── processor.log
├── file_processor.py # Lógica de procesamiento
├── api.py # Servidor FastAPI (backend)
├── question-2.component.ts/html/scss # Angular (frontend)
└── README.md


