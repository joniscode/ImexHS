import { Routes } from '@angular/router';
import { HomeComponent } from './features/home/home';

export const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  {
    path: 'question-1-hanoi',
    loadComponent: () =>
      import('./Question-1/hanoi.component').then(m => m.HanoiComponent),
  },
  {
    path: 'question-2-fileprocessor',
    loadComponent: () =>
      import('./Question-2/question-2.component').then((m) => m.Question2Component)
  }
];