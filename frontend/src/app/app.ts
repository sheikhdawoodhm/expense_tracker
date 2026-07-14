import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ExpenseTrackerComponent } from './components/expense-tracker/expense-tracker.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [CommonModule,RouterOutlet],
  template: '<router-outlet></router-outlet>'
})
export class App {
  protected readonly title = signal('expense-tracking-app');
}


