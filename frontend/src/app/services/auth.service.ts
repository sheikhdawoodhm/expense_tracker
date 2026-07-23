import { Injectable, signal, inject } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { ToastrService } from 'ngx-toastr';
import { tap } from 'rxjs/operators';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private router = inject(Router);
  private http = inject(HttpClient);
  private toastr = inject(ToastrService);

  private apiUrl = 'http://localhost:8000/api/auth';
  
  currentUser = signal<any | null>(null);
  isAuthenticated = signal<boolean>(false);

  constructor() {
    if (typeof localStorage !== 'undefined') {
      const saved = localStorage.getItem('auth_session');
      if (saved) {
        try {
          const parsed = JSON.parse(saved);
          this.currentUser.set(parsed);
          this.isAuthenticated.set(true);
        } catch (e) {}
      }
    }
  }

  login(email: string, psw: string) {
    if (email && psw) {
      this.http.post<{access_token: string, refresh_token: string, token_type: string}>(`${this.apiUrl}/login`, { email, password: psw }).subscribe({
        next: (res) => {
          const sessionData = { email, access_token: res.access_token, refresh_token: res.refresh_token };
          this.currentUser.set(sessionData);
          this.isAuthenticated.set(true);
          if (typeof localStorage !== 'undefined') {
            localStorage.setItem('auth_session', JSON.stringify(sessionData));
          }
          this.toastr.success('Logged in successfully', 'Success');
          this.router.navigate(['/dashboard']);
        },
        error: (err) => {
          const msg = err.error?.detail || 'Login failed';
          this.toastr.error(msg, 'Error');
          console.error(err);
        }
      });
    }
  }

  signup(email: string, psw: string) {
    if (email && psw) {
      this.http.post(`${this.apiUrl}/signup`, { email, password: psw }).subscribe({
        next: (res) => {
          this.toastr.success('Account created successfully. Please login.', 'Success');
          this.router.navigate(['/login']);
        },
        error: (err) => {
          const msg = err.error?.detail || 'Signup failed';
          this.toastr.error(msg, 'Error');
          console.error(err);
        }
      });
    }
  }

  refreshToken(): Observable<{access_token: string, refresh_token: string, token_type: string}> {
    const session = this.currentUser();
    return this.http.post<{access_token: string, refresh_token: string, token_type: string}>(`${this.apiUrl}/refresh`, { refresh_token: session?.refresh_token }).pipe(
      tap(res => {
        if (session) {
          const newSession = { ...session, access_token: res.access_token };
          this.currentUser.set(newSession);
          if (typeof localStorage !== 'undefined') {
            localStorage.setItem('auth_session', JSON.stringify(newSession));
          }
        }
      })
    );
  }

  logout() {
    this.http.post(`${this.apiUrl}/logout`, {}).subscribe({
      next: () => this.clearSession(),
      error: () => this.clearSession()
    });
  }

  private clearSession() {
    this.currentUser.set(null);
    this.isAuthenticated.set(false);
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem('auth_session');
    }
    this.toastr.info('Logged out successfully');
    this.router.navigate(['/login']);
  }
}