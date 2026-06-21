import { Component, Output, EventEmitter, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { debounceTime, distinctUntilChanged, Subject, switchMap, of, catchError } from 'rxjs';
import { environment } from '../../../environments/environment';

interface SearchResult {
  id: string;
  title: string;
  category: string;
  venue_name: string;
  coordinates: { longitude: number; latitude: number };
}

@Component({
  selector: 'app-search-bar',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="search-wrapper">
      <span class="search-icon">🔍</span>
      <input
        class="search-input"
        type="text"
        placeholder="Buscar eventos, artistas, venues..."
        [(ngModel)]="query"
        (ngModelChange)="onQueryChange($event)"
        (focus)="showResults.set(true)"
        (blur)="onBlur()"
      />
      @if (isLoading()) {
        <span class="search-spinner"></span>
      }
      @if (showResults() && results().length > 0) {
        <ul class="search-results">
          @for (r of results(); track r.id) {
            <li class="search-result-item" (mousedown)="select(r)">
              <span class="result-icon">{{ categoryIcon(r.category) }}</span>
              <div class="result-info">
                <div class="result-title">{{ r.title }}</div>
                <div class="result-sub">{{ r.venue_name }}</div>
              </div>
            </li>
          }
        </ul>
      }
    </div>
  `,
  styles: [`
    .search-wrapper {
      position: relative;
      flex: 1;
      display: flex;
      align-items: center;
    }
    .search-icon { position: absolute; left: 10px; font-size: 0.85rem; pointer-events: none; opacity: 0.5; }
    .search-input {
      width: 100%;
      padding: 7px 32px 7px 32px;
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 8px;
      color: #f1f5f9;
      font-size: 0.85rem;
      outline: none;
      transition: border-color 0.15s;
      &::placeholder { color: rgba(255,255,255,0.3); }
      &:focus { border-color: rgba(255,255,255,0.2); }
    }
    .search-spinner {
      position: absolute;
      right: 10px;
      width: 14px;
      height: 14px;
      border: 2px solid rgba(255,255,255,0.15);
      border-top-color: #7c3aed;
      border-radius: 50%;
      animation: spin 0.6s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .search-results {
      position: absolute;
      top: calc(100% + 8px);
      left: 0;
      right: 0;
      background: rgba(17,17,24,0.97);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 10px;
      overflow: hidden;
      list-style: none;
      margin: 0;
      padding: 4px;
      backdrop-filter: blur(16px);
      z-index: 50;
      max-height: 300px;
      overflow-y: auto;
    }
    .search-result-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 10px;
      border-radius: 7px;
      cursor: pointer;
      transition: background 0.1s;
      &:hover { background: rgba(255,255,255,0.07); }
    }
    .result-icon { font-size: 1rem; }
    .result-title { font-size: 0.83rem; font-weight: 600; color: #f1f5f9; }
    .result-sub { font-size: 0.72rem; color: rgba(255,255,255,0.4); }
  `],
})
export class SearchBarComponent {
  @Output() flyTo = new EventEmitter<{ lng: number; lat: number }>();

  query = '';
  results = signal<SearchResult[]>([]);
  isLoading = signal(false);
  showResults = signal(false);

  private search$ = new Subject<string>();

  constructor(private http: HttpClient) {
    this.search$.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap(q => {
        if (q.length < 2) { this.results.set([]); return of([]); }
        this.isLoading.set(true);
        return this.http.get<SearchResult[]>(`${environment.apiUrl}/events?q=${encodeURIComponent(q)}&limit=8`)
          .pipe(catchError(() => of([])));
      }),
    ).subscribe(res => {
      this.results.set(res as SearchResult[]);
      this.isLoading.set(false);
    });
  }

  onQueryChange(q: string): void {
    this.search$.next(q);
  }

  onBlur(): void {
    setTimeout(() => this.showResults.set(false), 150);
  }

  select(result: SearchResult): void {
    this.query = result.title;
    this.showResults.set(false);
    this.flyTo.emit({ lng: result.coordinates.longitude, lat: result.coordinates.latitude });
  }

  categoryIcon(cat: string): string {
    const map: Record<string, string> = {
      music: '🎵', visual_art: '🎨', theater: '🎭',
      cinema: '🎬', festival: '🎉', dance: '💃', workshop: '🛠️',
    };
    return map[cat] ?? '🎭';
  }
}
