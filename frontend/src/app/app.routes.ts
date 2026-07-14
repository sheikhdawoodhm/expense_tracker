import { Routes } from '@angular/router';
import { ExpenseTrackerComponent } from './components/expense-tracker/expense-tracker.component';
import { LoginComponent } from './components/login/login.component';
import { SignupComponent } from './components/signup/signup.components';
import { authGuard } from './guards/auth.guard';
import { AnalysisComponent } from './components/analysis/analysis.component.component';
import { LayoutComponent } from './components/layouts/layout.component';



export const routes: Routes = [
  
{ path: 'login', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  { 
    path: '', 
    component: LayoutComponent,
    canActivate: [authGuard], 
    children: [
      { path: 'dashboard', component: ExpenseTrackerComponent },
      { path: 'analysis', component: AnalysisComponent },
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' } 
    ]
  },

  
  { path: 'dashboard', component: ExpenseTrackerComponent, canActivate: [authGuard] },
  { path: 'analysis', component: AnalysisComponent, canActivate: [authGuard] },
  { path: '', redirectTo: '/login', pathMatch: 'full' }, 
  { path: '**', redirectTo: '/login' } 
];