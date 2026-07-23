import { Component, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-auth',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="auth-overlay">
      <div class="auth-card glass">
        <div class="auth-logo">🎭 ZoomArtists</div>
        <div class="auth-tabs">
          <button [class.active]="mode() === 'login'" (click)="mode.set('login')">Iniciar sesión</button>
          <button [class.active]="mode() === 'register'" (click)="mode.set('register')">Registrarse</button>
        </div>

        @if (mode() === 'register') {
          <input placeholder="Nombre" [(ngModel)]="name" class="auth-input" />
        }
        <input placeholder="Email" [(ngModel)]="email" type="email" class="auth-input" />

        @if (mode() === 'register') {
          <div class="role-picker">
            <span class="role-label">Quiero</span>
            <div class="role-seg">
              <button
                type="button"
                [class.active]="role() === 'attendee'"
                (click)="role.set('attendee')"
              >
                Descubrir eventos
              </button>
              <button
                type="button"
                [class.active]="role() === 'organizer'"
                (click)="role.set('organizer')"
              >
                Organizar eventos
              </button>
            </div>
          </div>
        }
        <input placeholder="Contraseña" [(ngModel)]="password" type="password" class="auth-input" />

        @if (error()) {
          <p class="auth-error">{{ error() }}</p>
        }

        <button class="auth-submit" (click)="submit()" [disabled]="isLoading()">
          {{ isLoading() ? 'Cargando...' : (mode() === 'login' ? 'Iniciar sesión' : 'Crear cuenta') }}
        </button>

        <button class="auth-back" (click)="goBack()">← Volver al mapa</button>
      </div>
    </div>
  `,
  styles: [`
    .auth-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.7);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 100;
    }
    .auth-card {
      width: min(400px, calc(100vw - 32px));
      padding: 32px;
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .auth-logo { font-size: 1.3rem; font-weight: 800; color: #f1f5f9; text-align: center; margin-bottom: 8px; }
    .auth-tabs { display: flex; gap: 0; border-radius: 8px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); }
    .auth-tabs button {
      flex: 1; padding: 8px; background: transparent; border: none; color: rgba(255,255,255,0.5);
      cursor: pointer; font-size: 0.85rem; transition: all 0.15s;
      &.active { background: rgba(255,255,255,0.1); color: #fff; font-weight: 600; }
    }
    .auth-input {
      padding: 10px 14px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
      border-radius: 8px; color: #f1f5f9; font-size: 0.88rem; outline: none;
      &::placeholder { color: rgba(255,255,255,0.3); }
      &:focus { border-color: #7c3aed; }
    }
    .auth-submit {
      padding: 11px; background: #7c3aed; border: none; border-radius: 10px; color: #fff;
      font-size: 0.9rem; font-weight: 700; cursor: pointer; margin-top: 4px; transition: opacity 0.15s;
      &:hover { opacity: 0.85; } &:disabled { opacity: 0.5; cursor: not-allowed; }
    }
    .auth-error { color: #ef4444; font-size: 0.8rem; text-align: center; margin: 0; }
    .auth-back { background: none; border: none; color: rgba(255,255,255,0.4); font-size: 0.8rem;
      cursor: pointer; text-align: center; &:hover { color: #fff; } }
    .role-picker { display: flex; flex-direction: column; gap: 6px; }
    .role-label { font-size: 0.75rem; color: rgba(255,255,255,0.4); }
    .role-seg {
      display: flex; gap: 4px; padding: 3px; border-radius: 9px;
      background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
    }
    .role-seg button {
      flex: 1; padding: 8px; background: none; border: none; border-radius: 6px;
      color: rgba(255,255,255,0.55); font-size: 0.8rem; cursor: pointer; transition: all 0.15s;
      &.active { background: #7c3aed; color: #fff; font-weight: 600; }
    }
  `],
})
export class AuthComponent {
  private authService = inject(AuthService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  mode = signal<'login' | 'register'>('login');
  role = signal<'attendee' | 'organizer'>('attendee');
  name = '';
  email = '';
  password = '';
  error = signal<string | null>(null);
  isLoading = signal(false);

  submit(): void {
    this.error.set(null);
    this.isLoading.set(true);
    const obs = this.mode() === 'login'
      ? this.authService.login(this.email, this.password)
      : this.authService.register(this.name, this.email, this.password, this.role());

    obs.subscribe({
      next: () => this.router.navigateByUrl(this.nextUrl()),
      error: (err) => {
        this.error.set(err?.error?.detail ?? 'Error al autenticar');
        this.isLoading.set(false);
      },
    });
  }

  private nextUrl(): string {
    const next = this.route.snapshot.queryParamMap.get('next');
    return next && next.startsWith('/') ? next : '/';
  }

  goBack(): void {
    this.router.navigate(['/']);
  }
}
