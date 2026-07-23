import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="h-screen overflow-hidden bg-[#0b0e14] text-white flex flex-col md:flex-row font-sans">
      
      
      <aside class="w-full md:w-64 shrink-0 bg-[#111827] border-b md:border-b-0 md:border-r border-[#1f2937] p-6 flex flex-col justify-between z-10 shadow-lg">
        <div>
          
          <div class="mb-8">
            <h1 class="text-xl font-bold bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
              Expense Tracking App
            </h1>
          </div>

          
          <nav class="space-y-2">
            <a routerLink="/dashboard" 
               routerLinkActive="bg-blue-600/20 text-blue-400 border-blue-500" 
               class="flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium text-gray-400 hover:text-white hover:bg-[#1f2937] transition-all border-l-2 border-transparent">
              <span>📊</span> Dashboard
            </a>

            <a routerLink="/analysis" 
               routerLinkActive="bg-emerald-600/20 text-emerald-400 border-emerald-500" 
               class="flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium text-gray-400 hover:text-white hover:bg-[#1f2937] transition-all border-l-2 border-transparent">
              <span>📈</span> Metrics Analytics
            </a>
          </nav>
        </div>

        
        <div class="mt-auto pt-6 border-t border-[#1f2937] flex items-center justify-between">
          <div class="truncate mr-2">
            <p class="text-xs text-gray-400 truncate">{{ authService.currentUser()?.email || 'Active Session' }}</p>
          </div>
          <button (click)="onLogout()" 
                  class="text-xs font-bold text-red-400 hover:text-red-500 bg-red-950/20 border border-red-500/20 px-2.5 py-1.5 rounded-md cursor-pointer transition-colors shrink-0">
            Sign out
          </button>
        </div>
      </aside>

      
      <main class="flex-1 p-6 md:p-8 overflow-y-auto">
        
        <router-outlet></router-outlet>
      </main>

    </div>
  `
})
export class LayoutComponent {
  protected authService = inject(AuthService);

  onLogout() {
    this.authService.logout();
  }
}