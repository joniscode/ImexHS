import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-question-3',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './question-3.component.html',
  styleUrls: ['./question-3.component.scss']
})
export class Question3Component {
  selectedFile: File | null = null;
  result: any = null;
  error: string = '';
  loading: boolean = false;

  constructor(private http: HttpClient) {}

  onFileChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      if (file.type === 'application/json' || file.name.endsWith('.json')) {
        this.selectedFile = file;
        this.error = '';
        this.result = null;
      } else {
        this.error = '❌ El archivo debe ser .json';
        this.selectedFile = null;
      }
    }
  }

  onUpload(): void {
    if (!this.selectedFile) return;

    const reader = new FileReader();
    reader.onload = () => {
      try {
        const jsonData = JSON.parse(reader.result as string);
        this.loading = true;
        this.result = null;
        this.error = '';

        this.http.post('http://localhost:8000/api/elements/', jsonData, { responseType: 'json' })
          .subscribe({
            next: res => {
              this.result = res;
              this.loading = false;
            },
            error: err => {
              this.error = '❌ Error al procesar el archivo JSON.';
              this.loading = false;
            }
          });

      } catch (e) {
        this.error = '❌ El contenido del archivo no es un JSON válido.';
        this.selectedFile = null;
      }
    };

    reader.readAsText(this.selectedFile);
  }

  clear(): void {
    this.selectedFile = null;
    this.result = null;
    this.error = '';
    this.loading = false;
  }
}
