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
      import('./Question-2/question-2.component').then(m => m.Question2Component),
  },
  {
    path: 'question-3-api',
    loadComponent: () =>
      import('./Question-3/question-3.component').then(m => m.Question3Component),
  },
  {
    path: 'question-4-stain',
    loadComponent: () => import('./Question-4/question-4.component')
                        .then(m => m.Question4Component),
  },
  {
    path: 'question-4-angular-app',
    redirectTo: 'question-4-stain',
  }
];