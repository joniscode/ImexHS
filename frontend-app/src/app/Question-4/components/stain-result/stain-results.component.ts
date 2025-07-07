import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StainCalculation } from '../../models/stain-area.model';

@Component({
  selector: 'app-stain-results',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="p-4">
      <h2 class="text-xl font-bold mb-4">📋 Historial de resultados</h2>
      <table class="w-full border">
        <thead>
          <tr class="bg-gray-200">
            <th class="border px-2">#</th>
            <th class="border px-2">Ancho</th>
            <th class="border px-2">Alto</th>
            <th class="border px-2">Puntos</th>
            <th class="border px-2">Dentro</th>
            <th class="border px-2">Área estimada</th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let r of results; let i = index">
            <td class="border px-2">{{ i + 1 }}</td>
            <td class="border px-2">{{ r.width }}</td>
            <td class="border px-2">{{ r.height }}</td>
            <td class="border px-2">{{ r.totalPoints }}</td>
            <td class="border px-2">{{ r.pointsInside }}</td>
            <td class="border px-2">{{ r.estimatedArea | number:'1.0-2' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  `,
  styles: []
})
export class StainResultsComponent {
  results: StainCalculation[] = [];

  ngOnInit() {
    const stored = localStorage.getItem('stain_results');
    if (stored) {
      this.results = JSON.parse(stored);
    }
  }
}