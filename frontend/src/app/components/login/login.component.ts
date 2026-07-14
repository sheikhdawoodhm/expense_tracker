import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="min-h-screen bg-[#0b0e14] flex items-center justify-center p-4 font-sans text-white">
      <div class="w-full max-w-md bg-[#111827] border border-[#1f2937] p-8 rounded-2xl shadow-2xl">
        <h2 class="text-2xl font-bold text-center text-blue-500 mb-2">Welcome Back</h2>
        <p class="text-xs text-gray-400 text-center mb-6">Log in to manage your live aggregate allocations</p>
        
        <form (ngSubmit)="onLogin()" class="space-y-4">
          <div>
            <label class="block text-xs text-gray-400 mb-1">Email Address</label>
            <input type="email" [(ngModel)]="email" name="email" required autocomplete="off"
                   class="w-full p-2.5 bg-[#1f2937] border border-[#374151] rounded-md focus:border-blue-500 focus:outline-none text-sm"/>
          </div>
          <div>
            <label class="block text-xs text-gray-400 mb-1">Password</label>
            <input type="password" [(ngModel)]="password" name="password" required
                   class="w-full p-2.5 bg-[#1f2937] border border-[#374151] rounded-md focus:border-blue-500 focus:outline-none text-sm"/>
          </div>
          <button type="submit" class="w-full p-3 bg-blue-600 hover:bg-blue-700 font-bold rounded-md transition-colors cursor-pointer text-sm mt-2">
            Sign In
          </button>
        </form>
        <p class="text-xs text-center text-gray-400 mt-6">
          Don't have an account? <a routerLink="/signup" class="text-blue-400 hover:underline cursor-pointer">Register here</a>
        </p>
      </div>
    </div>
  `
})
export class LoginComponent {
  private authService = inject(AuthService);
  email = '';
  password = '';

  onLogin() {
    this.authService.login(this.email, this.password);
  }
}