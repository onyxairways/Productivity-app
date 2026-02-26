import { Routes } from '@angular/router';
import { TaskListComponent } from './task-list/task-list';

export const routes: Routes = [
  { path: '', component: TaskListComponent },
  { path: 'tasks/:id', loadComponent: () =>
      import('./task-detail/task-detail').then(m => m.TaskDetailComponent)
  }
];
