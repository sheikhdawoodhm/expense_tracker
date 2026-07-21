import { Injectable, signal, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

// Matching your HTML tabs: expense, asset, liability
export type TrackerType = 'expense' | 'asset' | 'liability';

export interface TrackerItem {
  id?: number; 
  amount: number;
  type: TrackerType;
  category: string;
  description: string;       // Maps to your backend DB column
  transaction_date: string;  // Maps to your backend DB column
}

@Injectable({
  providedIn: 'root'
})
export class LedgerService {
  private http = inject(HttpClient);
  private apiUrl = 'http://127.0.0.1:8000/api/expenses';
  
  items = signal<TrackerItem[]>([]);

  fetchItems(): Observable<TrackerItem[]> {
    return this.http.get<TrackerItem[]>(this.apiUrl).pipe(
      tap(data => this.items.set(data))
    );
  }

  addItem(item: TrackerItem): Observable<TrackerItem> {
    return this.http.post<TrackerItem>(this.apiUrl, item).pipe(
      tap(() => this.fetchItems().subscribe())
    );
  }

  updateItem(id: number, item: TrackerItem): Observable<TrackerItem> {
    return this.http.put<TrackerItem>(`${this.apiUrl}/${id}`, item).pipe(
      tap(() => this.fetchItems().subscribe())
    );
  }

  deleteItem(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`).pipe(
      tap(() => this.fetchItems().subscribe())
    );
  }
}