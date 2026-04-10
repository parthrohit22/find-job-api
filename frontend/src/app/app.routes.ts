import { Routes } from '@angular/router';

import { authChildGuard, authGuard } from './core/guards/auth.guard';
import { ShellLayoutComponent } from './layout/shell-layout.component';
import { ActivityPageComponent } from './pages/activity/activity-page.component';
import { JobDetailPageComponent } from './pages/job-detail/job-detail-page.component';
import { LoginPageComponent } from './pages/login/login-page.component';
import { SavedPageComponent } from './pages/saved/saved-page.component';
import { SearchPageComponent } from './pages/search/search-page.component';

export const routes: Routes = [
  {
    path: 'login',
    component: LoginPageComponent
  },
  {
    path: '',
    component: ShellLayoutComponent,
    canActivate: [authGuard],
    canActivateChild: [authChildGuard],
    children: [
      {
        path: '',
        pathMatch: 'full',
        redirectTo: 'search'
      },
      {
        path: 'search',
        component: SearchPageComponent
      },
      {
        path: 'saved',
        component: SavedPageComponent
      },
      {
        path: 'activity',
        component: ActivityPageComponent
      },
      {
        path: 'roles/:id',
        component: JobDetailPageComponent
      }
    ]
  },
  {
    path: '**',
    redirectTo: 'search'
  }
];
