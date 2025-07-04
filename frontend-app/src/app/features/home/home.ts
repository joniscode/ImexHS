import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [NgFor],
  templateUrl: './home.html',
  styleUrls: ['./home.scss']
})
export class HomeComponent {
  pills = [
    { title: '🧩 Recursión y Colores', link: '/question-1-hanoi' },
    { title: '📂 Procesador de Archivos', link: '/question-2-fileprocessor' },
    { title: '🔗 API Resultados Médicos', link: '/question-3-api' },
    { title: '🧮 Área de Mancha', link: '/question-4-angular-app' }
  ];

  openLink(url: string) {
    window.open(url, '_blank');
  }
}
