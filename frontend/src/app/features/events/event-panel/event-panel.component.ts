import { Component, computed, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { animate, style, transition, trigger } from '@angular/animations';
import { EventService } from '../../../core/services/event.service';
import { AuthService } from '../../../core/services/auth.service';
import { CATEGORY_COLORS, CATEGORY_ICONS, CATEGORY_LABELS } from '../../../core/models/event.model';

@Component({
  selector: 'app-event-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './event-panel.component.html',
  styleUrl: './event-panel.component.scss',
  animations: [
    trigger('slideIn', [
      transition(':enter', [
        style({ transform: 'translateX(100%)', opacity: 0 }),
        animate('320ms cubic-bezier(0.25, 0.46, 0.45, 0.94)', style({ transform: 'translateX(0)', opacity: 1 })),
      ]),
      transition(':leave', [
        animate('250ms ease-in', style({ transform: 'translateX(100%)', opacity: 0 })),
      ]),
    ]),
  ],
})
export class EventPanelComponent {
  eventService = inject(EventService);
  authService = inject(AuthService);

  event = this.eventService.selectedEvent;
  isLoadingEvent = this.eventService.isLoadingEvent;
  currentUser = this.authService.currentUser;

  // Top events shown as a list summary when nothing is selected — nearest first.
  topEvents = computed(() =>
    [...this.eventService.nearbyEvents()].sort(
      (a, b) => (a.distance_meters ?? Infinity) - (b.distance_meters ?? Infinity),
    ),
  );

  expandedArtistId: string | null = null;

  openEvent(id: string): void {
    this.eventService.openPanel(id);
  }

  categoryColor(cat: string): string {
    return CATEGORY_COLORS[cat as keyof typeof CATEGORY_COLORS] ?? '#7c3aed';
  }

  categoryIcon(cat: string): string {
    return CATEGORY_ICONS[cat as keyof typeof CATEGORY_ICONS] ?? '🎭';
  }

  categoryLabel(cat: string): string {
    return CATEGORY_LABELS[cat as keyof typeof CATEGORY_LABELS] ?? cat;
  }

  formatDate(date: string): string {
    return new Date(date).toLocaleDateString('es-MX', {
      weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
    });
  }

  formatTime(date: string): string {
    return new Date(date).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
  }

  formatDistance(meters: number | null): string {
    if (!meters) return '';
    return meters < 1000 ? `${Math.round(meters)} m` : `${(meters / 1000).toFixed(1)} km`;
  }

  toggleArtist(id: string): void {
    this.expandedArtistId = this.expandedArtistId === id ? null : id;
  }

  saveEvent(): void {
    const ev = this.event();
    if (!ev) return;
    this.eventService.saveEvent(ev.id).subscribe();
  }

  share(): void {
    const ev = this.event();
    if (!ev) return;
    const url = `${window.location.origin}/?event=${ev.id}`;
    if (navigator.share) {
      navigator.share({ title: ev.title, url });
    } else {
      navigator.clipboard.writeText(url);
    }
  }

  close(): void {
    this.eventService.closePanel();
  }

  googleMapsUrl(venue: { coordinates: { latitude: number; longitude: number } }): string {
    return `https://maps.google.com/?q=${venue.coordinates.latitude},${venue.coordinates.longitude}`;
  }
}
