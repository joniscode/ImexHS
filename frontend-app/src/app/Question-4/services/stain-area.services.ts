import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { StainCalculation } from '../models/stain-area.model';

@Injectable({ providedIn: 'root' })
export class StainAreaService {
  private historySubject = new BehaviorSubject<StainCalculation[]>([]);
  history$ = this.historySubject.asObservable();

  private canvas: HTMLCanvasElement = document.createElement('canvas');
  private ctx = this.canvas.getContext('2d')!;

  loadImage(file: File): Promise<ImageData> {
    return new Promise((resolve, reject) => {
      const img = new Image();
      const reader = new FileReader();

      reader.onload = () => {
        img.onload = () => {
          this.canvas.width = img.width;
          this.canvas.height = img.height;
          this.ctx.drawImage(img, 0, 0);
          const imageData = this.ctx.getImageData(0, 0, img.width, img.height);
          resolve(imageData);
        };
        img.onerror = reject;
        img.src = reader.result as string;
      };

      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  calculateArea(imageData: ImageData, nPoints: number, file: File): StainCalculation {
    const { width, height, data } = imageData;
    let insideStain = 0;

    for (let i = 0; i < nPoints; i++) {
      const x = Math.floor(Math.random() * width);
      const y = Math.floor(Math.random() * height);
      const idx = (y * width + x) * 4;
      const isWhite = data[idx] === 255 && data[idx + 1] === 255 && data[idx + 2] === 255;
      if (isWhite) insideStain++;
    }

    const totalArea = width * height;
    const estimatedArea = (insideStain / nPoints) * totalArea;

    const result: StainCalculation = {
      id: crypto.randomUUID(),
      imageName: file.name,
      width,
      height,
      totalPoints: nPoints,
      pointsInside: insideStain,
      estimatedArea,
      timestamp: new Date().toISOString()
    };

    const current = this.historySubject.getValue();
    const updated = [result, ...current];
    this.historySubject.next(updated);
    localStorage.setItem('stain_results', JSON.stringify(updated));

    return result;
  }
}
