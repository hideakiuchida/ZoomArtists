import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { VenueCreatePayload, VenueResponse } from '../models/venue.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class VenueService {
  private http = inject(HttpClient);
  private readonly API = environment.apiUrl;

  venues = signal<VenueResponse[]>([]);

  list(): Observable<VenueResponse[]> {
    return this.http
      .get<VenueResponse[]>(`${this.API}/venues`)
      .pipe(tap(venues => this.venues.set(venues)));
  }

  create(payload: VenueCreatePayload): Observable<VenueResponse> {
    return this.http
      .post<VenueResponse>(`${this.API}/venues`, payload)
      .pipe(tap(venue => this.venues.update(list => [...list, venue])));
  }
}
