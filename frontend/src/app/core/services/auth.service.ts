import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { switchMap, tap } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { User, TokenResponse, UserRole } from '../models/user.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly API = environment.apiUrl;

  currentUser = signal<User | null>(null);
  isLoggedIn = signal(false);

  constructor(private http: HttpClient, private router: Router) {
    const stored = localStorage.getItem('user');
    if (stored && this.getAccessToken()) {
      this.currentUser.set(JSON.parse(stored));
      this.isLoggedIn.set(true);
    }
  }

  login(email: string, password: string): Observable<User> {
    return this.http.post<TokenResponse>(`${this.API}/auth/login`, { email, password }).pipe(
      tap(tokens => this.persistTokens(tokens)),
      switchMap(() => this.fetchMe()),
    );
  }

  register(
    name: string,
    email: string,
    password: string,
    role: Extract<UserRole, 'attendee' | 'organizer'> = 'attendee',
  ): Observable<User> {
    return this.http
      .post<TokenResponse>(`${this.API}/auth/register`, { name, email, password, role })
      .pipe(
        tap(tokens => this.persistTokens(tokens)),
        switchMap(() => this.fetchMe()),
      );
  }

  isOrganizer(): boolean {
    const role = this.currentUser()?.role;
    return role === 'organizer' || role === 'admin' || role === 'artist';
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    this.currentUser.set(null);
    this.isLoggedIn.set(false);
    this.router.navigate(['/']);
  }

  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  fetchMe(): Observable<User> {
    return this.http.get<User>(`${this.API}/auth/me`).pipe(
      tap(user => {
        this.currentUser.set(user);
        localStorage.setItem('user', JSON.stringify(user));
      }),
    );
  }

  private persistTokens(tokens: TokenResponse): void {
    localStorage.setItem('access_token', tokens.access_token);
    localStorage.setItem('refresh_token', tokens.refresh_token);
    this.isLoggedIn.set(true);
  }
}
