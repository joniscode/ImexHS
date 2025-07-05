import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-recursive-box',
  standalone: true,
  imports: [CommonModule, RecursiveBoxComponent],
  templateUrl: './recursive-box.component.html',
  styleUrls: ['./recursive-box.component.scss']
})
export class RecursiveBoxComponent {
  @Input() depth = 0;

  colors = ['#ffdada', '#ffd6a5', '#fdffb6', '#caffbf', '#9bf6ff', '#a0c4ff', '#bdb2ff', '#ffc6ff'];

  getColor(): string {
    return this.colors[this.depth % this.colors.length];
  }
}
