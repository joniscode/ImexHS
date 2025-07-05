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
  csvFile = '';
  csvSummary = false;
  dicomFile = '';
  extractImage = false;
  dicomImageUrl: string = '';
  reportReady = false;

  // 📤 Resultados
  result = '';
  loading = false;
  dicomFiles: string[] = [];
  csvFiles: string[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadDicomFiles();
    this.loadCsvFiles();
  }

  loadDicomFiles() {
    this.http.get<string[]>('http://localhost:8000/list-dicoms')
      .subscribe({
        next: res => this.dicomFiles = res,
        error: err => console.error("Error cargando archivos DICOM", err)
      });
  }

  loadCsvFiles() {
    this.http.get<string[]>('http://localhost:8000/list-csvs')
      .subscribe({
        next: res => this.csvFiles = res,
        error: err => console.error("Error cargando archivos CSV", err)
      });
  }

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
  this.reportReady = false;
  this.http.post('http://localhost:8000/read-csv', {
    filename: this.csvFile,
    summary: this.csvSummary,
    report_path: 'reports'
  }, { responseType: 'text' }).subscribe({
    next: res => {
      this.result = res;
      this.loading = false;
      if (this.csvSummary) this.reportReady = true; // habilita el botón
    },
    error: err => {
      this.result = '❌ Error al leer el archivo CSV.';
      this.loading = false;
    }
  });
}

  onReadDicom() {
  this.loading = true;
  this.result = '';
  this.dicomImageUrl = '';  // Reinicia

  this.http.post('http://localhost:8000/read-dicom', {
    filename: this.dicomFile,
    tags: [
      [0x0010, 0x0010],  // Paciente
      [0x0008, 0x0060]   // Modalidad
    ],
    extract_image: this.extractImage
  }, { responseType: 'text' }).subscribe({
    next: res => {
      this.result = res;
      this.loading = false;
      if (this.extractImage) {
        const imageName = this.dicomFile.replace('.dcm', '.png');
        this.dicomImageUrl = `http://localhost:8000/output/${imageName}`;
      }
    },
    error: err => {
      this.result = '❌ Error al leer el archivo DICOM.';
      this.loading = false;
    }
  });
}

  downloadReport() {
    window.open('http://localhost:8000/reports/csv_report.txt', '_blank');
  }

  get dicomImagePath(): string {
    return this.extractImage ? `http://localhost:8000/output/${this.dicomFile.replace('.dcm', '.png')}` : '';
  }
}
