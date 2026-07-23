import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

export interface GoalSettings {
  goalName: string;
  goalTargetAmount: number;
  monthlySavingsContribution: number;
}

export interface CategorySpendingDetail {
  category: string;
  totalAmount: number;
  percentageOfTotalExpenses: number;
}

export interface AnalyticsOverview {
  totalAssets: number;
  totalLiabilities: number;
  totalExpenses: number;
  netWorth: number;
  healthySpendingScore: number;
  ringStrokeOffset: number;
  categoryWiseSpending: CategorySpendingDetail[];
  monthsToReachGoal: number;
  targetVariance: number;
  settings: GoalSettings;
}

@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/api/analytics';

  overview = signal<AnalyticsOverview | null>(null);

  loadOverview(): Observable<AnalyticsOverview> {
    return this.http.get<AnalyticsOverview>(`${this.apiUrl}/`).pipe(
      tap(data => this.overview.set(data))
    );
  }

  updateGoalSettings(settings: GoalSettings): Observable<GoalSettings> {
    return this.http.put<GoalSettings>(`${this.apiUrl}/settings`, settings).pipe(
      tap(() => {
        this.loadOverview().subscribe();
      })
    );
  }
}