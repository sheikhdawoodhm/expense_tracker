import { Component, inject, OnInit, OnDestroy, signal, computed, NgZone } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AnalyticsService } from '../../services/analytics.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-analysis',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './analysis.component.html'
})
export class AnalysisComponent implements OnInit, OnDestroy {
  private analyticsService = inject(AnalyticsService);
  private zone = inject(NgZone);
  private authService = inject(AuthService);

  private overviewRaw = this.analyticsService.overview;

  goalName = signal('Emergency Fund Cushion');
  goalTargetAmount = signal(50000);
  monthlySavingsContribution = signal(2500);

  private eventSource!: EventSource;

  ngOnInit(): void {
    this.loadData();
    this.setupSSE();
  }

  private loadData(): void {
    this.analyticsService.loadOverview().subscribe(data => {
      if (data?.settings) {
        this.goalName.set(data.settings.goalName);
        this.goalTargetAmount.set(data.settings.goalTargetAmount);
        this.monthlySavingsContribution.set(data.settings.monthlySavingsContribution);
      }
    });
  }

  private setupSSE(): void {
    const session = this.authService.currentUser();
    const token = session?.access_token || '';
    this.eventSource = new EventSource(`http://localhost:8000/api/analytics/stream?token=${token}`);
    this.eventSource.onmessage = (event) => {
      this.zone.run(() => {
        this.loadData();
      });
    };
  }

  ngOnDestroy(): void {
    if (this.eventSource) {
      this.eventSource.close();
    }
  }

  totalAssets = computed(() => this.overviewRaw()?.totalAssets ?? 0);
  totalLiabilities = computed(() => this.overviewRaw()?.totalLiabilities ?? 0);
  totalExpenses = computed(() => this.overviewRaw()?.totalExpenses ?? 0);
  netWorth = computed(() => this.overviewRaw()?.netWorth ?? 0);

  healthySpendingScore = computed(() => this.overviewRaw()?.healthySpendingScore ?? 0);
  ringStrokeOffset = computed(() => this.overviewRaw()?.ringStrokeOffset ?? 251.32);

  categoryWiseSpending = computed(() => this.overviewRaw()?.categoryWiseSpending ?? []);

  monthsToReachGoal = computed(() => {
    const gapNeeded = this.goalTargetAmount() - this.netWorth();
    const monthlyContribution = this.monthlySavingsContribution();

    if (gapNeeded <= 0 || monthlyContribution <= 0) return 0;
    return Math.ceil(gapNeeded / monthlyContribution);
  });

  targetVariance = computed(() => {
    const diff = this.goalTargetAmount() - this.netWorth();
    return diff > 0 ? diff : 0;
  });

  saveGoalSettings(): void {
    this.analyticsService.updateGoalSettings({
      goalName: this.goalName(),
      goalTargetAmount: this.goalTargetAmount(),
      monthlySavingsContribution: this.monthlySavingsContribution()
    }).subscribe();
  }
}