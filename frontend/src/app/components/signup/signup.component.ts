import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="min-h-screen bg-[#0b0e14] flex items-center justify-center p-4 font-sans text-white">
      <div class="w-full max-w-md bg-[#111827] border border-[#1f2937] p-8 rounded-2xl shadow-2xl">
        <h2 class="text-2xl font-bold text-center text-green-500 mb-2">Create Account</h2>
        <p class="text-xs text-gray-400 text-center mb-6">Get tracking your assets, expenses, and liabilities</p>
        
        <form (ngSubmit)="signupForm.valid && onSignup()" #signupForm="ngForm" class="space-y-4">
          <div>
            <label class="block text-xs text-gray-400 mb-1">Email Address</label>
            <input type="email" [(ngModel)]="email" name="email" required autocomplete="off"
                   pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$" #emailRef="ngModel"
                   class="w-full p-2.5 bg-[#1f2937] border border-[#374151] rounded-md focus:border-green-500 focus:outline-none text-sm"/>
            @if (emailRef.invalid && (emailRef.dirty || emailRef.touched)) {
              <div class="text-red-500 text-[10px] mt-1">Please enter a valid email address.</div>
            }
          </div>
          <div>
            <label class="block text-xs text-gray-400 mb-1">Create Password</label>
            <div class="relative">
              <input [type]="showPassword ? 'text' : 'password'" [(ngModel)]="password" name="password" required
                     minlength="6" #passwordRef="ngModel"
                     class="w-full p-2.5 bg-[#1f2937] border border-[#374151] rounded-md focus:border-green-500 focus:outline-none text-sm pr-10"/>
              <button type="button" (click)="showPassword = !showPassword" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white cursor-pointer focus:outline-none">
                @if (showPassword) {
                  <!-- Open Eye -->
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                  </svg>
                } @else {
                  <!-- Closed Eye (with slash) -->
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                  </svg>
                }
              </button>
            </div>
            @if (passwordRef.invalid && (passwordRef.dirty || passwordRef.touched)) {
              <div class="text-red-500 text-[10px] mt-1">Password must be at least 6 characters.</div>
            }
          </div>
          <button type="submit" [disabled]="signupForm.invalid" class="w-full p-3 bg-green-600 hover:bg-green-700 disabled:bg-green-800 disabled:opacity-50 font-bold rounded-md transition-colors cursor-pointer text-sm mt-2">
            Register Account
          </button>
        </form>
        <p class="text-xs text-center text-gray-400 mt-6">
          Already verified? <a routerLink="/login" class="text-green-400 hover:underline cursor-pointer">Sign in instead</a>
        </p>
      </div>
    </div>
  `
})
export class SignupComponent {
  private authService = inject(AuthService);
  email = '';
  password = '';
  showPassword = false;

  onSignup() {
    this.authService.signup(this.email, this.password);
  }
}