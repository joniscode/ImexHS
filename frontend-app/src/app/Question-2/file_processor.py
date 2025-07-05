import os
import csv
import logging
from typing import Optional, List, Tuple
import statistics
import pydicom
from PIL import Image
import numpy as np

class FileProcessor:
    def __init__(self, base_path: str, log_file: str):
        self.base_path = os.path.abspath(base_path)
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logging.basicConfig(filename=log_file, level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def list_folder_contents(self, folder_name: str, details: bool = False) -> str:
        full_path = os.path.abspath(os.path.join(self.base_path, folder_name))
        try:
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"No existe la carpeta: {full_path}")

            entries = os.listdir(full_path)
            files = [f for f in entries if os.path.isfile(os.path.join(full_path, f))]
            dirs = [d for d in entries if os.path.isdir(os.path.join(full_path, d))]

            lines = [f"📂 Carpeta: {full_path}", f"📦 Elementos: {len(entries)}", "📄 Archivos:"]
            for f in files:
                path = os.path.join(full_path, f)
                if details:
                    size = os.path.getsize(path) / (1024 * 1024)
                    mtime = os.path.getmtime(path)
                    lines.append(f"  - {f} ({size:.2f} MB, Últ. modificado: {mtime})")
                else:
                    lines.append(f"  - {f}")
            lines.append("📁 Subcarpetas:")
            lines.extend(f"  - {d}" for d in dirs)
            return "\n".join(lines)
        except Exception as e:
            self.logger.error(f"Error reading folder '{folder_name}': {e}")
            return f"❌ Error: {e}"

    def read_csv(self, filename: str, report_path: Optional[str] = None, summary: bool = False) -> str:
        try:
            file_path = os.path.join(self.base_path, filename)
            with open(file_path, newline='', encoding='utf-8', errors='replace') as csvfile:
                reader = list(csv.DictReader(csvfile))
                lines = [f"📊 Filas: {len(reader)}"]
                if reader:
                    lines.append(f"🧾 Columnas: {list(reader[0].keys())}")
                    numeric_data = {}
                    for row in reader:
                        for key, val in row.items():
                            try:
                                numeric_data.setdefault(key, []).append(float(val))
                            except ValueError:
                                continue

                    report_lines = []
                    for key, values in numeric_data.items():
                        avg = statistics.mean(values)
                        std = statistics.stdev(values) if len(values) > 1 else 0
                        line = f"📈 {key}: Prom = {avg:.2f}, Desv = {std:.2f}"
                        report_lines.append(line)
                        lines.append(line)

                    if summary:
                        for key in reader[0].keys():
                            values = [row[key] for row in reader]
                            if not all(v.replace('.', '', 1).isdigit() for v in values):
                                freq = {v: values.count(v) for v in set(values)}
                                lines.append(f"📜 {key}: {freq}")

                    if report_path:
                        os.makedirs(report_path, exist_ok=True)
                        with open(os.path.join(report_path, "csv_report.txt"), "w") as report_file:
                            report_file.write("\n".join(report_lines))
                return "\n".join(lines)
        except Exception as e:
            self.logger.error(f"Error reading CSV '{filename}': {e}")
            return f"❌ Error: {e}"

    def read_dicom(self, filename: str, tags: Optional[List[Tuple[int, int]]] = None, extract_image: bool = False) -> str:
        try:
            path = os.path.join(self.base_path, filename)
            ds = pydicom.dcmread(path, force=True)
            lines = [
                f"🧠 Nombre del paciente: {ds.get('PatientName', 'No disponible')}",
                f"🗓️ Fecha del estudio: {ds.get('StudyDate', 'No disponible')}",
                f"🧪 Modalidad: {ds.get('Modality', 'No disponible')}"
            ]
            if tags:
                for group, element in tags:
                    tag_value = ds.get((group, element), "No encontrado")
                    lines.append(f"🏷️ Tag {hex(group)}, {hex(element)}: {tag_value}")
            if extract_image and hasattr(ds, 'pixel_array'):
                os.makedirs("output", exist_ok=True)
                img = Image.fromarray(ds.pixel_array)
                img.save(os.path.join("output", filename.replace(".dcm", ".png")))
                lines.append("🖼️ Imagen guardada en /output")
            return "\n".join(lines)
        except Exception as e:
            self.logger.error(f"Error reading DICOM '{filename}': {e}")
            return f"❌ Error: {e}"

    def list_dicom_files(self) -> List[str]:
        try:
            return [f for f in os.listdir(self.base_path) if f.lower().endswith('.dcm')]
        except Exception as e:
            self.logger.error(f"Error listing DICOM files: {e}")
            return []

    def list_csv_files(self) -> List[str]:
        try:
            return [f for f in os.listdir(self.base_path) if f.lower().endswith('.csv')]
        except Exception as e:
            self.logger.error(f"Error listing CSV files: {e}")
            return []
