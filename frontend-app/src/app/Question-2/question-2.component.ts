import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-question-2',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './question-2.component.html',
  styleUrls: ['./question-2.component.scss']
})
export class Question2Component {
  // 📥 Inputs del formulario
  folderName = '';
  showDetails = false;
  csvFile = 'sample-02-csv.csv';
  csvSummary = false;
  dicomFile = 'sample-02-dicom.dcm';
  extractImage = false;

  // 📤 Resultados
  result = '';
  loading = false;

  constructor(private http: HttpClient) {}

  onListFolder() {
    this.loading = true;
    this.result = '';
    this.http.post('http://localhost:8000/list-folder', {
      folder_name: this.folderName,
      details: this.showDetails
    }, { responseType: 'text' }).subscribe({
      next: res => { this.result = res; this.loading = false; },
      error: err => { this.result = '❌ Error al listar carpeta.'; this.loading = false; }
    });
  }

  onReadCsv() {
    this.loading = true;
    this.result = '';
    this.http.post('http://localhost:8000/read-csv', {
      filename: this.csvFile,
      summary: this.csvSummary,
      report_path: 'reports'
    }, { responseType: 'text' }).subscribe({
      next: res => { this.result = res; this.loading = false; },
      error: err => { this.result = '❌ Error al leer el archivo CSV.'; this.loading = false; }
    });
  }

  onReadDicom() {
    this.loading = true;
    this.result = '';
    this.http.post('http://localhost:8000/read-dicom', {
      filename: this.dicomFile,
      tags: [
        [0x0010, 0x0010],  // Paciente
        [0x0008, 0x0060]   // Modalidad
      ],
      extract_image: this.extractImage
    }, { responseType: 'text' }).subscribe({
      next: res => { this.result = res; this.loading = false; },
      error: err => { this.result = '❌ Error al leer el archivo DICOM.'; this.loading = false; }
    });
  }
}
