# Ejercicio 3 – REST CRUD de Resultados Médicos

Angular 17 + FastAPI + SQLite  
Puerto back-end **8000** · Puerto front-end **4200**

---

## Qué hace

1. **Sube** un archivo JSON con varios registros de resultados de imágenes médicas.  
2. El API (FastAPI) valida, normaliza y calcula promedios antes/después.  
3. Guarda/actualiza cada registro en SQLite.  
4. El front muestra una **tabla con scroll**; puedes filtrar, editar o eliminar registros sin el ID y registros que no deberian ser cambiantes si no por el contrario fijos.

---

## Requisitos

| Herramienta | Versión |
|-------------|---------|
| Python      | ≥ 3.9   |
| Node.js     | ≥ 18    |
| pip         | ≥ 22    |
| Angular CLI | ≥ 17    |

---

## Instalación rápida

```bash
# 1. Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt      # fastapi, uvicorn, sqlalchemy, pydantic

uvicorn medical_api:app --reload --port 8000
# DB se crea en data/medical_data.db

# 2. Frontend
cd ../frontend-app
npm install              # o pnpm install
ng serve                 # http://localhost:4200