import { Routes } from '@angular/router';
import { organizerGuard } from './core/guards/organizer.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./features/map/map.component').then(m => m.MapComponent),
  },
  {
    path: 'auth',
    loadComponent: () => import('./features/auth/auth.component').then(m => m.AuthComponent),
  },
  {
    path: 'organizer',
    canActivate: [organizerGuard],
    loadComponent: () =>
      import('./features/organizer/organizer-dashboard/organizer-dashboard.component').then(
        m => m.OrganizerDashboardComponent,
      ),
  },
  {
    path: 'organizer/events/new',
    canActivate: [organizerGuard],
    loadComponent: () =>
      import('./features/organizer/event-form/event-form.component').then(
        m => m.EventFormComponent,
      ),
  },
  {
    path: 'organizer/events/:id/edit',
    canActivate: [organizerGuard],
    loadComponent: () =>
      import('./features/organizer/event-form/event-form.component').then(
        m => m.EventFormComponent,
      ),
  },
  { path: '**', redirectTo: '' },
];
