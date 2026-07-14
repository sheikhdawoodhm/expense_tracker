import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { LedgerService } from '../../services/ledger.service'; 

@Component({
  selector: 'app-analysis',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './analysis.component.html'
})
export class AnalysisComponent {
  private ledgerService = inject(LedgerService);
  
  
  items = this.ledgerService.items;

  
  goalName = signal('Emergency Fund Cushion');
  goalTargetAmount = signal(50000);
  monthlySavingsContribution = signal(2500);

  
  
  
  totalAssets = computed(() => {
    return this.items().filter(i => i.type === 'asset').reduce((sum, item) => sum + item.amount, 0);
  });

  totalLiabilities = computed(() => {
    return this.items().filter(i => i.type === 'liability').reduce((sum, item) => sum + item.amount, 0);
  });

  totalExpenses = computed(() => {
    return this.items().filter(i => i.type === 'expense').reduce((sum, item) => sum + item.amount, 0);
  });

  netWorth = computed(() => this.totalAssets() - this.totalLiabilities());

  
  
  
  healthySpendingScore = computed(() => {
    const assets = this.totalAssets();
    if (assets === 0) return 0; 

    
    
    const burnRatio = (this.totalExpenses() / assets) * 100;
    const computedScore = 100 - (burnRatio * 3); 
    return Math.max(0, Math.min(Math.round(computedScore), 100)); 
  });

  ringStrokeOffset = computed(() => {
    const circumference = 2 * Math.PI * 40; 
    return circumference - (this.healthySpendingScore() / 100) * circumference;
  });

  
  
  
  categoryWiseSpending = computed(() => {
    
    const expenses = this.items().filter(i => i.type === 'expense');
    const groups: { [key: string]: number } = {};

    
    expenses.forEach(item => {
      groups[item.category] = (groups[item.category] || 0) + item.amount;
    });

    return Object.keys(groups).map(categoryName => ({
      category: categoryName,
      totalAmount: groups[categoryName],
      percentageOfTotalExpenses: this.totalExpenses() > 0 ? (groups[categoryName] / this.totalExpenses()) * 100 : 0
    }));
  });

  
  
  
  monthsToReachGoal = computed(() => {
    const gapNeeded = this.goalTargetAmount() - this.netWorth();
    const monthlyContribution = this.monthlySavingsContribution();

    if (gapNeeded <= 0) return 0; 
    if (monthlyContribution <= 0) return 0; 

    return Math.ceil(gapNeeded / monthlyContribution);
  });
}