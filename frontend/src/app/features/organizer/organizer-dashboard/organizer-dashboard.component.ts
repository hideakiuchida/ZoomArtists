import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { EventService } from '../../../core/services/event.service';
import { AuthService } from '../../../core/services/auth.service';
import {
  CATEGORY_COLORS,
  CATEGORY_ICONS,
  CATEGORY_LABELS,
  EventResponse,
  EventStatus,
} from '../../../core/models/event.model';

const STATUS_LABELS: Record<EventStatus, string> = {
  draft: 'Borrador',
  pending: 'En revisión',
  published: 'Publicado',
  cancelled: 'Cancelado',
  past: 'Finalizado',
};

@Component({
  selector: 'app-organizer-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './organizer-dashboard.component.html',
  styleUrl: './organizer-dashboard.component.scss',
})
export class OrganizerDashboardComponent implements OnInit {
  private eventService = inject(EventService);
  private auth = inject(AuthService);
  private router = inject(Router);

  readonly CATEGORY_ICONS = CATEGORY_ICONS;
  readonly CATEGORY_LABELS = CATEGORY_LABELS;
  readonly CATEGORY_COLORS = CATEGORY_COLORS;
  readonly STATUS_LABELS = STATUS_LABELS;

  events = signal<EventResponse[]>([]);
  loading = signal(true);
  error = signal<string | null>(null);
  busyId = signal<string | null>(null);

  userName = computed(() => this.auth.currentUser()?.name ?? 'Organizador');

  stats = computed(() => {
    const list = this.events();
    return {
      total: list.length,
      published: list.filter(e => e.status === 'published').length,
      review: list.filter(e => e.status === 'draft' || e.status === 'pending').length,
    };
  });

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.error.set(null);
    this.eventService.listMine().subscribe({
      next: events => {
        this.events.set(events);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('No pudimos cargar tus eventos. Intenta de nuevo.');
        this.loading.set(false);
      },
    });
  }

  publish(event: EventResponse): void {
    this.busyId.set(event.id);
    this.eventService.update(event.id, { status: 'published' }).subscribe({
      next: updated => {
        this.events.update(list => list.map(e => (e.id === updated.id ? updated : e)));
        this.busyId.set(null);
      },
      error: () => {
        this.error.set('No se pudo publicar el evento.');
        this.busyId.set(null);
      },
    });
  }

  remove(event: EventResponse): void {
    if (!confirm(`¿Eliminar "${event.title}"? Esta acción no se puede deshacer.`)) return;
    this.busyId.set(event.id);
    this.eventService.remove(event.id).subscribe({
      next: () => {
        this.events.update(list => list.filter(e => e.id !== event.id));
        this.busyId.set(null);
      },
      error: () => {
        this.error.set('No se pudo eliminar el evento.');
        this.busyId.set(null);
      },
    });
  }

  edit(event: EventResponse): void {
    this.router.navigate(['/organizer/events', event.id, 'edit']);
  }

  logout(): void {
    this.auth.logout();
  }

  formatDate(iso: string): string {
    return new Date(iso).toLocaleDateString('es-PE', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  }

  categoryColor(event: EventResponse): string {
    return this.CATEGORY_COLORS[event.category];
  }
}
