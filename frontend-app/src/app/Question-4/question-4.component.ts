import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTabsModule } from '@angular/material/tabs';
import { StainUploaderComponent } from './components/stain-uploader/stain-uploader.component';
import { StainResultsComponent } from './components/stain-result/stain-results.component';

@Component({
  selector: 'app-question4',
  standalone: true,
  imports: [
    CommonModule,
    MatTabsModule,
    StainUploaderComponent,
    StainResultsComponent
  ],
  template: `
    <mat-tab-group>
      <mat-tab label="Calcular área">
        <app-stain-uploader></app-stain-uploader>
      </mat-tab>

      <mat-tab label="Historial">
        <app-stain-results></app-stain-results>
      </mat-tab>

      <mat-tab label="Metodología">
      </mat-tab>
    </mat-tab-group>
  `
})
export class Question4Component {}
