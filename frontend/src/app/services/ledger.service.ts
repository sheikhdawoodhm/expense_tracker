import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

export type TrackerType = 'expense' | 'asset' | 'liability';

export interface TrackerItem {
  id: number; // Matches PostgreSQL SERIAL PK
  type: TrackerType;
  title: string;
  amount: number;
  category: string;
  description?: string;
  date: string;
}

@Injectable({
  providedIn: 'root'
})


export class LedgerService {
  private http = inject(HttpClient);
private apiUrl = 'http://localhost:8000/api/expenses';
  items = signal<TrackerItem[]>([]);

  /** Syncs local signal store with database */
  loadItems(): Observable<TrackerItem[]> {
    return this.http.get<TrackerItem[]>(this.apiUrl).pipe(
      tap(data => this.items.set(data))
    );
  }

  addItem(item: Omit<TrackerItem, 'id'>): Observable<TrackerItem> {
    return this.http.post<TrackerItem>(this.apiUrl, item).pipe(
      tap(created => this.items.update(prev => [created, ...prev]))
    );
  }

  updateItem(id: number, item: Omit<TrackerItem, 'id'>): Observable<TrackerItem> {
    return this.http.put<TrackerItem>(`${this.apiUrl}/${id}`, item).pipe(
      tap(updated => {
        this.items.update(prev => prev.map(i => i.id === id ? updated : i));
      })
    );
  }

  deleteItem(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`).pipe(
      tap(() => {
        this.items.update(prev => prev.filter(i => i.id !== id));
      })
    );
  }


}