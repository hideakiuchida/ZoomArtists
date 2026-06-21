import { Injectable, signal } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import {
  EventResponse,
  EventSummary,
  NearbyEventsQuery,
  NearbyEventsResponse,
} from '../models/event.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class EventService {
  private readonly API = environment.apiUrl;

  selectedEvent = signal<EventResponse | null>(null);
  nearbyEvents = signal<EventSummary[]>([]);
  isPanelOpen = signal(false);

  constructor(private http: HttpClient) {}

  getNearby(query: NearbyEventsQuery): Observable<NearbyEventsResponse> {
    let params = new HttpParams()
      .set('lat', query.lat)
      .set('lng', query.lng)
      .set('radius', query.radius ?? 5000)
      .set('limit', query.limit ?? 50);

    if (query.category) params = params.set('category', query.category);
    if (query.is_free !== undefined) params = params.set('is_free', query.is_free);
    if (query.cursor) params = params.set('cursor', query.cursor);

    return this.http.get<NearbyEventsResponse>(`${this.API}/events/nearby`, { params }).pipe(
      tap(res => this.nearbyEvents.set(res.events)),
    );
  }

  getById(id: string): Observable<EventResponse> {
    return this.http.get<EventResponse>(`${this.API}/events/${id}`).pipe(
      tap(event => this.selectedEvent.set(event)),
    );
  }

  openPanel(id: string): void {
    this.isPanelOpen.set(true);
    this.getById(id).subscribe();
  }

  closePanel(): void {
    this.isPanelOpen.set(false);
    this.selectedEvent.set(null);
  }

  saveEvent(id: string): Observable<void> {
    return this.http.post<void>(`${this.API}/events/${id}/save`, {});
  }

  unsaveEvent(id: string): Observable<void> {
    return this.http.delete<void>(`${this.API}/events/${id}/save`);
  }
}
