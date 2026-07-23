import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { of } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { EventService } from '../../../core/services/event.service';
import { VenueService } from '../../../core/services/venue.service';
import {
  CATEGORY_COLORS,
  CATEGORY_ICONS,
  CATEGORY_LABELS,
  EventCategory,
  EventCreatePayload,
  EventStatus,
  EventUpdatePayload,
} from '../../../core/models/event.model';
import { VenueResponse } from '../../../core/models/venue.model';

interface CategoryOption {
  value: EventCategory;
  label: string;
  icon: string;
  color: string;
}

const STATUS_OPTIONS: { value: EventStatus; label: string }[] = [
  { value: 'draft', label: 'Borrador' },
  { value: 'published', label: 'Publicado' },
  { value: 'cancelled', label: 'Cancelado' },
];

@Component({
  selector: 'app-event-form',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './event-form.component.html',
  styleUrl: './event-form.component.scss',
})
export class EventFormComponent implements OnInit {
  private eventService = inject(EventService);
  private venueService = inject(VenueService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  readonly categories: CategoryOption[] = (
    Object.keys(CATEGORY_LABELS) as EventCategory[]
  ).map(value => ({
    value,
    label: CATEGORY_LABELS[value],
    icon: CATEGORY_ICONS[value],
    color: CATEGORY_COLORS[value],
  }));
  readonly statusOptions = STATUS_OPTIONS;
  readonly currencies = ['PEN', 'USD', 'MXN'];

  mode = signal<'create' | 'edit'>('create');
  loading = signal(true);
  saving = signal(false);
  error = signal<string | null>(null);
  venues = signal<VenueResponse[]>([]);

  private eventId: string | null = null;

  // ── Form model (template-driven) ──────────────────────────────────────────
  title = '';
  category: EventCategory | null = null;
  description = '';
  startDate = '';
  endDate = '';
  venueMode: 'existing' | 'new' = 'existing';
  venueId = '';
  existingVenueName = '';
  status: EventStatus = 'draft';

  // New venue sub-form
  vName = '';
  vAddress = '';
  vCity = 'Lima';
  vCountry = 'Perú';
  vLat: number | null = null;
  vLng: number | null = null;

  // Ticketing
  isFree = false;
  ticketPrice: number | null = null;
  currency = 'PEN';
  ticketUrl = '';

  // Extras
  capacity: number | null = null;
  tags = '';
  videoUrl = '';

  pageTitle = computed(() =>
    this.mode() === 'edit' ? 'Editar evento' : 'Crear evento',
  );

  ngOnInit(): void {
    this.eventId = this.route.snapshot.paramMap.get('id');

    this.venueService.list().subscribe({
      next: venues => this.venues.set(venues),
      error: () => this.venues.set([]),
    });

    if (this.eventId) {
      this.mode.set('edit');
      this.eventService.getById(this.eventId).subscribe({
        next: event => {
          this.title = event.title;
          this.category = event.category;
          this.description = event.description ?? '';
          this.startDate = this.toLocalInput(event.start_date);
          this.endDate = event.end_date ? this.toLocalInput(event.end_date) : '';
          this.venueId = event.venue.id;
          this.existingVenueName = event.venue.name;
          this.isFree = event.is_free;
          this.ticketPrice = event.ticket_price;
          this.currency = event.currency ?? 'PEN';
          this.ticketUrl = event.ticket_url ?? '';
          this.capacity = event.capacity;
          this.tags = event.tags.join(', ');
          this.videoUrl = event.video_url ?? '';
          this.status = event.status === 'past' ? 'published' : event.status;
          this.loading.set(false);
        },
        error: () => {
          this.error.set('No pudimos cargar el evento.');
          this.loading.set(false);
        },
      });
    } else {
      this.loading.set(false);
    }
  }

  selectCategory(cat: EventCategory): void {
    this.category = cat;
  }

  private validate(): string | null {
    if (!this.title.trim()) return 'El título es obligatorio.';
    if (!this.category) return 'Elige una categoría.';
    if (!this.startDate) return 'Indica la fecha de inicio.';
    if (this.mode() === 'create') {
      if (this.venueMode === 'existing' && !this.venueId) return 'Selecciona un lugar.';
      if (this.venueMode === 'new') {
        if (!this.vName.trim() || !this.vAddress.trim()) {
          return 'Completa el nombre y la dirección del nuevo lugar.';
        }
        if (this.vLat === null || this.vLng === null) {
          return 'Ingresa las coordenadas (latitud y longitud) del lugar.';
        }
      }
    }
    if (!this.isFree && this.ticketPrice !== null && this.ticketPrice < 0) {
      return 'El precio no puede ser negativo.';
    }
    return null;
  }

  private parsedTags(): string[] {
    return this.tags
      .split(',')
      .map(t => t.trim())
      .filter(Boolean);
  }

  private num(value: number | null): number | null {
    if (value === null || (value as unknown as string) === '') return null;
    return Number(value);
  }

  submit(): void {
    const problem = this.validate();
    if (problem) {
      this.error.set(problem);
      return;
    }
    this.error.set(null);
    this.saving.set(true);

    if (this.mode() === 'edit' && this.eventId) {
      const payload: EventUpdatePayload = {
        title: this.title.trim(),
        description: this.description.trim() || null,
        category: this.category!,
        start_date: this.startDate,
        end_date: this.endDate || null,
        is_free: this.isFree,
        ticket_price: this.isFree ? null : this.num(this.ticketPrice),
        ticket_url: this.isFree ? null : this.ticketUrl.trim() || null,
        capacity: this.num(this.capacity),
        tags: this.parsedTags(),
        status: this.status,
      };
      this.eventService.update(this.eventId, payload).subscribe({
        next: () => this.router.navigate(['/organizer']),
        error: err => this.fail(err),
      });
      return;
    }

    // Create — ensure a venue exists first, then create the event.
    const venue$ =
      this.venueMode === 'new'
        ? this.venueService.create({
            name: this.vName.trim(),
            address: this.vAddress.trim(),
            city: this.vCity.trim(),
            country: this.vCountry.trim(),
            coordinates: { latitude: Number(this.vLat), longitude: Number(this.vLng) },
          })
        : of({ id: this.venueId } as VenueResponse);

    venue$
      .pipe(
        switchMap(venue => {
          const payload: EventCreatePayload = {
            title: this.title.trim(),
            description: this.description.trim() || null,
            category: this.category!,
            start_date: this.startDate,
            end_date: this.endDate || null,
            venue_id: venue.id,
            is_free: this.isFree,
            ticket_price: this.isFree ? null : this.num(this.ticketPrice),
            ticket_url: this.isFree ? null : this.ticketUrl.trim() || null,
            currency: this.currency,
            capacity: this.num(this.capacity),
            tags: this.parsedTags(),
            video_url: this.videoUrl.trim() || null,
          };
          return this.eventService.create(payload);
        }),
      )
      .subscribe({
        next: () => this.router.navigate(['/organizer']),
        error: err => this.fail(err),
      });
  }

  private fail(err: unknown): void {
    const detail = (err as { error?: { detail?: string } })?.error?.detail;
    this.error.set(detail ?? 'No se pudo guardar. Revisa los datos e intenta de nuevo.');
    this.saving.set(false);
  }

  cancel(): void {
    this.router.navigate(['/organizer']);
  }

  private toLocalInput(iso: string): string {
    const d = new Date(iso);
    const pad = (n: number) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(
      d.getHours(),
    )}:${pad(d.getMinutes())}`;
  }
}
