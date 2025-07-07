import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-question-2',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './question-2.component.html',
  styleUrls: ['./question-2.component.scss'],
})
export class Question2Component implements OnInit {

  /* ---------------- estado ---------------- */
  folderName = '';
  showDetails = false;

  csvFile = '';
  csvSummary = false;

  dicomFile = '';
  extractImage = false;

  dicomImageUrl = '';
  reportReady   = false;

  result  = '';
  loading = false;

  csvFiles:   string[] = [];
  dicomFiles: string[] = [];

  /* -------------- helpers --------------- */
  private readonly API = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  /* ciclo de vida */
  ngOnInit(): void {
    this.refreshFileLists();
  }

  /* ──────────────── LISTAS ──────────────── */
  private refreshFileLists(): void {
    this.loadCsvFiles();
    this.loadDicomFiles();
  }

  private loadCsvFiles(): void {
    this.http.get<string[]>(`${this.API}/list-csvs`)
      .subscribe({
        next: res => this.csvFiles = res,
        error: err => console.error('❌ Error list-csvs', err)
      });
  }

  private loadDicomFiles(): void {
    this.http.get<string[]>(`${this.API}/list-dicoms`)
      .subscribe({
        next: res => this.dicomFiles = res,
        error: err => console.error('❌ Error list-dicoms', err)
      });
  }

  /* ──────────────── LISTAR CARPETA ─────────────── */
  onListFolder(): void {
    this.loading = true;
    this.result  = '';

    this.http.post(
      `${this.API}/list-folder`,
      { folder_name: this.folderName, details: this.showDetails },
      { responseType: 'text' }
    ).subscribe({
      next: res => {
        this.result  = res;
        this.loading = false;
        /*  🔄  actualiza combos después de listar  */
        this.refreshFileLists();
      },
      error: ()  => {
        this.result  = '❌ Error al listar carpeta.';
        this.loading = false;
      }
    });
  }

  /* ──────────────── CSV ─────────────── */
  onReadCsv(): void {
    this.loading = true;
    this.result  = '';
    this.reportReady = false;

    this.http.post(
      `${this.API}/read-csv`,
      { filename: this.csvFile, summary: this.csvSummary, report_path: 'reports' },
      { responseType: 'text' }
    ).subscribe({
      next: res => {
        this.result      = res;
        this.loading     = false;
        this.reportReady = this.csvSummary;
      },
      error: () => {
        this.result  = '❌ Error al leer CSV.';
        this.loading = false;
      }
    });
  }

  /* ──────────────── DICOM ─────────────── */
  onReadDicom(): void {
    this.loading      = true;
    this.result       = '';
    this.dicomImageUrl = '';

    this.http.post(
      `${this.API}/read-dicom`,
      {
        filename: this.dicomFile,
        tags: [[0x0010, 0x0010], [0x0008, 0x0060]],
        extract_image: this.extractImage
      },
      { responseType: 'text' }
    ).subscribe({
      next: res => {
        this.result  = res;
        this.loading = false;
        if (this.extractImage) {
          this.dicomImageUrl =
            `${this.API}/output/${this.dicomFile.replace('.dcm', '.png')}`;
        }
      },
      error: () => {
        this.result  = '❌ Error al leer DICOM.';
        this.loading = false;
      }
    });
  }

  /* descargar informe */
  downloadReport(): void {
    window.open(`${this.API}/reports/csv_report.txt`, '_blank');
  }
}
