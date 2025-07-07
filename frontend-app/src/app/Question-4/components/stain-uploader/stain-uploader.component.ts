import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { StainCalculation } from '../../models/stain-area.model';
import { StainAreaService } from '../../services/stain-area.services';

@Component({
  selector: 'app-stain-uploader',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './stain-uploader.component.html',
  styleUrls: ['./stain-uploader.component.scss']
})
export class StainUploaderComponent {
  pointCount = 1000;
  selectedFile: File | null = null;
  previewUrl: string | null = null;
  loading = false;
  result: StainCalculation | null = null;
  errorMessage: string | null = null;

  constructor(private stainService: StainAreaService) {}

  onFileChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (!input.files || input.files.length === 0) {
      this.selectedFile = null;
      this.previewUrl = null;
      return;
    }

    const file = input.files[0];
    this.selectedFile = file;
    this.errorMessage = null;

    const reader = new FileReader();
    reader.onload = () => {
      this.previewUrl = reader.result as string;
    };
    reader.onerror = () => {
      this.errorMessage = 'Error al cargar la imagen.';
    };
    reader.readAsDataURL(file);
  }

  onCalculateArea(): void {
    if (!this.selectedFile) return;

    this.loading = true;
    this.errorMessage = null;
    this.result = null;

    this.stainService.loadImage(this.selectedFile)
      .then(imageData => {
        const result = this.stainService.calculateArea(imageData, this.pointCount, this.selectedFile!);
        this.result = result;
        this.loading = false;
      })
      .catch(err => {
        this.errorMessage = 'Ocurrió un error procesando la imagen.';
        console.error(err);
        this.loading = false;
      });
  }

  area(): number | null {
    return this.result?.estimatedArea ?? null;
  }

  error(): string | null {
    return this.errorMessage;
  }
}