import { Injectable, signal, inject } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private router = inject(Router);

  
  currentUser = signal<any | null>(null);
  isAuthenticated = signal<boolean>(false);

  login(email: string, psw: string) {
    if (email && psw) {
      
      this.currentUser.set({ email, uid: 'user_' + crypto.randomUUID() });
      this.isAuthenticated.set(true);
      this.router.navigate(['/dashboard']);
    }
  }

  signup(email: string, psw: string) {
    if (email && psw) {
      
      this.currentUser.set({ email, uid: 'user_' + crypto.randomUUID() });
      this.isAuthenticated.set(true);
      this.router.navigate(['/dashboard']);
    }
  }

  logout() {
    this.currentUser.set(null);
    this.isAuthenticated.set(false);
    this.router.navigate(['/login']);
  }
}