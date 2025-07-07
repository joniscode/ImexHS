import os
import csv
import logging
import statistics
from typing import Optional, List, Tuple

import pydicom
from PIL import Image
import numpy as np


class FileProcessor:
    """Clase utilitaria para operaciones con carpetas, CSV y DICOM."""

    def __init__(self, base_path: str, log_file: str):
        # Carpeta raíz para las operaciones
        self.base_path = os.path.abspath(base_path)

        # Configuración de logging
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logging.basicConfig(filename=log_file, level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    # ────────────────────────────────────────────────────────────────
    # 1. Listar contenido de carpetas
    # ────────────────────────────────────────────────────────────────
    def list_folder_contents(self, folder_name: str, details: bool = False) -> str:
        full_path = os.path.abspath(os.path.join(self.base_path, folder_name))
        try:
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"No existe la carpeta: {full_path}")

            entries = os.listdir(full_path)
            files = [f for f in entries if os.path.isfile(os.path.join(full_path, f))]
            dirs  = [d for d in entries if os.path.isdir(os.path.join(full_path, d))]

            lines = [
                f"📂 Carpeta: {full_path}",
                f"📦 Elementos: {len(entries)}",
                "📄 Archivos:",
            ]
            for f in files:
                path = os.path.join(full_path, f)
                if details:
                    size_mb = os.path.getsize(path) / (1024 * 1024)
                    mtime   = os.path.getmtime(path)
                    lines.append(f"  • {f}  ({size_mb:.2f} MB, Últ. modif: {mtime})")
                else:
                    lines.append(f"  • {f}")

            lines.append("📁 Subcarpetas:")
            lines.extend(f"  • {d}" for d in dirs)
            return "\n".join(lines)

        except Exception as e:
            self.logger.error(f"Error leyendo la carpeta '{folder_name}': {e}")
            return f"❌ Error: {e}"

    # ────────────────────────────────────────────────────────────────
    # 2. Leer y analizar CSV
    # ────────────────────────────────────────────────────────────────
    def read_csv(
        self,
        filename: str,
        report_path: Optional[str] = None,
        summary: bool = False,
    ) -> str:
        try:
            file_path = os.path.join(self.base_path, filename)
            with open(file_path, newline="", encoding="utf-8", errors="replace") as csvfile:
                reader = list(csv.DictReader(csvfile))
                lines  = [f"📊 Filas: {len(reader)}"]

                if reader:
                    lines.append(f"🧾 Columnas: {list(reader[0].keys())}")

                    numeric_data: dict[str, List[float]] = {}
                    for row in reader:
                        for key, val in row.items():
                            try:
                                numeric_data.setdefault(key, []).append(float(val))
                            except ValueError:
                                continue  # No numérico

                    report_lines: list[str] = []
                    for key, values in numeric_data.items():
                        avg = statistics.mean(values)
                        std = statistics.stdev(values) if len(values) > 1 else 0
                        line = f"📈 {key}: Prom = {avg:.2f}, Desv = {std:.2f}"
                        report_lines.append(line)
                        lines.append(line)

                    # Resumen de columnas NO numéricas
                    if summary:
                        for key in reader[0].keys():
                            values = [row[key] for row in reader]
                            if not all(v.replace(".", "", 1).isdigit() for v in values):
                                freq = {v: values.count(v) for v in set(values)}
                                lines.append(f"📜 {key}: {freq}")

                    # Guardar reporte, si se solicitó
                    if report_path:
                        rpt_dir = (
                            report_path
                            if os.path.isabs(report_path)
                            else os.path.join(self.base_path, report_path)
                        )
                        os.makedirs(rpt_dir, exist_ok=True)
                        with open(os.path.join(rpt_dir, "csv_report.txt"), "w", encoding="utf-8") as f:
                            f.write("\n".join(report_lines))

                return "\n".join(lines)

        except Exception as e:
            self.logger.error(f"Error leyendo CSV '{filename}': {e}")
            return f"❌ Error: {e}"

    # ────────────────────────────────────────────────────────────────
    # 3. Leer DICOM
    # ────────────────────────────────────────────────────────────────
    def read_dicom(
        self,
        filename: str,
        tags: Optional[List[Tuple[int, int]]] = None,
        extract_image: bool = False,
    ) -> str:
        try:
            path = os.path.join(self.base_path, filename)
            ds   = pydicom.dcmread(path, force=True)

            lines = [
                f"🧠 Nombre del paciente: {ds.get('PatientName', 'No disponible')}",
                f"🗓️ Fecha del estudio: {ds.get('StudyDate', 'No disponible')}",
                f"🧪 Modalidad: {ds.get('Modality', 'No disponible')}",
            ]

            # Tags adicionales
            if tags:
                for group, element in tags:
                    val = ds.get((group, element), "No encontrado")
                    lines.append(f"🏷️ Tag {hex(group)}, {hex(element)}: {val}")

            # Guardar imagen
            if extract_image and hasattr(ds, "pixel_array"):
                out_dir = os.path.join(self.base_path, "output")
                os.makedirs(out_dir, exist_ok=True)

                arr = ds.pixel_array.astype(float)
                # Normaliza a 8-bits si es 12/16 bits
                if arr.max() > 255:
                    arr = 255 * (arr - arr.min()) / (arr.max() - arr.min())
                img = Image.fromarray(arr.astype("uint8"))
                img_path = os.path.join(out_dir, filename.replace(".dcm", ".png"))
                img.save(img_path)
                lines.append(f"🖼️ Imagen guardada en {img_path}")

            return "\n".join(lines)

        except Exception as e:
            self.logger.error(f"Error leyendo DICOM '{filename}': {e}")
            return f"❌ Error: {e}"

    # ────────────────────────────────────────────────────────────────
    # 4. Listar archivos utilitarios
    # ────────────────────────────────────────────────────────────────
    def list_dicom_files(self) -> List[str]:
        try:
            return [f for f in os.listdir(self.base_path) if f.lower().endswith(".dcm")]
        except Exception as e:
            self.logger.error(f"Error listando DICOMs: {e}")
            return []

    def list_csv_files(self) -> List[str]:
        try:
            return [f for f in os.listdir(self.base_path) if f.lower().endswith(".csv")]
        except Exception as e:
            self.logger.error(f"Error listando CSVs: {e}")
            return []
