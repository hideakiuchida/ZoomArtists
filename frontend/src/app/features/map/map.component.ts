import {
  Component,
  OnInit,
  OnDestroy,
  ElementRef,
  ViewChild,
  signal,
  effect,
  inject,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import * as maplibregl from 'maplibre-gl';

import { EventService } from '../../core/services/event.service';
import { GeolocationService } from '../../core/services/geolocation.service';
import { EventSummary, EventCategory, CATEGORY_COLORS, CATEGORY_ICONS } from '../../core/models/event.model';
import { EventPanelComponent } from '../events/event-panel/event-panel.component';
import { SearchBarComponent } from '../search/search-bar.component';

type RadiusOption = 1000 | 5000 | 10000 | 25000;

@Component({
  selector: 'app-map',
  standalone: true,
  imports: [CommonModule, EventPanelComponent, SearchBarComponent],
  templateUrl: './map.component.html',
  styleUrl: './map.component.scss',
})
export class MapComponent implements OnInit, OnDestroy {
  @ViewChild('mapContainer', { static: true }) mapContainer!: ElementRef<HTMLDivElement>;

  private map!: maplibregl.Map;
  private markers = new Map<string, maplibregl.Marker>();
  private popupRef: maplibregl.Popup | null = null;

  private readonly RING_SOURCE = 'search-radius';
  private ringReady = false;
  private pulseFrame: number | null = null;

  private eventService = inject(EventService);
  private geoService = inject(GeolocationService);

  selectedRadius = signal<RadiusOption>(5000);
  activeCategory = signal<EventCategory | null>(null);
  isLoading = signal(false);

  readonly radiusOptions: { value: RadiusOption; label: string }[] = [
    { value: 1000, label: '1 km' },
    { value: 5000, label: '5 km' },
    { value: 10000, label: '10 km' },
    { value: 25000, label: '25 km' },
  ];

  readonly categories: { value: EventCategory; icon: string }[] = [
    { value: 'music', icon: '🎵' },
    { value: 'visual_art', icon: '🎨' },
    { value: 'theater', icon: '🎭' },
    { value: 'cinema', icon: '🎬' },
    { value: 'festival', icon: '🎉' },
    { value: 'dance', icon: '💃' },
  ];

  isPanelOpen = this.eventService.isPanelOpen;
  nearbyEvents = this.eventService.nearbyEvents;

  constructor() {
    effect(() => {
      const events = this.nearbyEvents();
      this.updateMarkers(events);
    });
  }

  async ngOnInit(): Promise<void> {
    const pos = await this.geoService.requestLocation();
    this.initMap(pos.lng, pos.lat);
    this.loadEvents(pos.lat, pos.lng);
  }

  private initMap(lng: number, lat: number): void {
    this.map = new maplibregl.Map({
      container: this.mapContainer.nativeElement,
      style: 'https://tiles.openfreemap.org/styles/dark',
      center: [lng, lat],
      zoom: 13,
    });

    this.map.addControl(new maplibregl.NavigationControl(), 'bottom-right');

    this.map.on('load', () => {
      this.addRadiusLayers();
      this.updateRadiusRing();
      this.startRingPulse();
    });

    this.map.on('moveend', () => {
      const center = this.map.getCenter();
      this.updateRadiusRing();
      this.loadEvents(center.lat, center.lng);
    });

    this.map.on('click', () => {
      if (this.popupRef) {
        this.popupRef.remove();
        this.popupRef = null;
      }
    });
  }

  private loadEvents(lat: number, lng: number): void {
    this.isLoading.set(true);
    this.eventService
      .getNearby({ lat, lng, radius: this.selectedRadius(), category: this.activeCategory() ?? undefined })
      .subscribe({ complete: () => this.isLoading.set(false) });
  }

  private updateMarkers(events: EventSummary[]): void {
    // Remove stale markers
    const incomingIds = new Set(events.map(e => e.id));
    for (const [id, marker] of this.markers) {
      if (!incomingIds.has(id)) {
        marker.remove();
        this.markers.delete(id);
      }
    }

    // Add new markers
    for (const event of events) {
      if (this.markers.has(event.id)) continue;

      const color = CATEGORY_COLORS[event.category];
      const icon = CATEGORY_ICONS[event.category];

      const el = document.createElement('div');
      el.className = 'event-marker';
      el.setAttribute('data-category', event.category);
      el.innerHTML = `<span class="marker-icon">${icon}</span>`;
      el.style.setProperty('--marker-color', color);

      el.addEventListener('click', (e) => {
        e.stopPropagation();
        this.showPopup(event);
      });

      const marker = new maplibregl.Marker({ element: el })
        .setLngLat([event.coordinates.longitude, event.coordinates.latitude])
        .addTo(this.map);

      this.markers.set(event.id, marker);
    }
  }

  private showPopup(event: EventSummary): void {
    if (this.popupRef) this.popupRef.remove();

    // The popup content is rendered as an Angular component via a portal-like approach
    // For now we use a lightweight HTML string; the full panel opens on "Ver detalles"
    const color = CATEGORY_COLORS[event.category];
    const icon = CATEGORY_ICONS[event.category];
    const price = event.is_free ? 'Gratis' : `$${event.ticket_price} ${event.currency}`;
    const date = new Date(event.start_date).toLocaleDateString('es-MX', {
      weekday: 'short', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit',
    });
    const dist = event.distance_meters ? `${(event.distance_meters / 1000).toFixed(1)} km` : '';

    const html = `
      <div class="event-popup-card" style="--accent:${color}">
        <div class="popup-category">${icon} ${event.category.replace('_', ' ').toUpperCase()}</div>
        <div class="popup-title">${event.title}</div>
        <div class="popup-meta">📍 ${event.venue_name}${dist ? ' · ' + dist : ''}</div>
        <div class="popup-meta">📅 ${date}</div>
        <div class="popup-meta">💰 ${price}</div>
        <div class="popup-actions">
          <button class="popup-btn-primary" id="popup-detail-${event.id}">Ver detalles →</button>
        </div>
      </div>
    `;

    this.popupRef = new maplibregl.Popup({ closeButton: false, maxWidth: '280px', offset: 12 })
      .setLngLat([event.coordinates.longitude, event.coordinates.latitude])
      .setHTML(html)
      .addTo(this.map);

    // The popup DOM exists immediately after addTo; attach the click handler to
    // the popup's own element so it survives regardless of event timing.
    const popupEl = this.popupRef.getElement();
    const detailBtn = popupEl?.querySelector(`#popup-detail-${event.id}`);
    detailBtn?.addEventListener('click', () => {
      this.eventService.openPanel(event.id);
      this.popupRef?.remove();
    });
  }

  setRadius(radius: RadiusOption): void {
    this.selectedRadius.set(radius);
    if (!this.map) return;
    // Resize the ring immediately, then zoom the map so the chosen radius fills
    // the view. fitBounds fires `moveend`, which reloads events with the new radius.
    this.updateRadiusRing();
    const c = this.map.getCenter();
    this.map.fitBounds(this.radiusBounds(c.lng, c.lat, radius), { padding: 80, duration: 800 });
  }

  setCategory(cat: EventCategory | null): void {
    this.activeCategory.set(cat);
    this.updateRadiusRing(); // re-tint the ring to the active category color
    const center = this.map?.getCenter();
    if (center) this.loadEvents(center.lat, center.lng);
  }

  /* ── Search-radius ring ──────────────────────────────────────────────────── */

  // A square bounding box that exactly circumscribes the radius circle, used to
  // frame the map at the right zoom for each radius option.
  private radiusBounds(lng: number, lat: number, radius: number): maplibregl.LngLatBoundsLike {
    const dLat = radius / 111_320;
    const dLng = radius / (111_320 * Math.cos((lat * Math.PI) / 180));
    return [
      [lng - dLng, lat - dLat],
      [lng + dLng, lat + dLat],
    ];
  }

  // Approximate a geographic circle as a polygon for rendering on the map.
  private metersToCircle(lng: number, lat: number, radius: number, points = 72): any {
    const coords: [number, number][] = [];
    const earth = 6_378_137;
    const latRad = (lat * Math.PI) / 180;
    for (let i = 0; i <= points; i++) {
      const theta = (i / points) * 2 * Math.PI;
      const dLng = ((radius * Math.cos(theta)) / (earth * Math.cos(latRad))) * (180 / Math.PI);
      const dLat = ((radius * Math.sin(theta)) / earth) * (180 / Math.PI);
      coords.push([lng + dLng, lat + dLat]);
    }
    return { type: 'Feature', geometry: { type: 'Polygon', coordinates: [coords] }, properties: {} };
  }

  private ringColor(): string {
    const cat = this.activeCategory();
    return cat ? CATEGORY_COLORS[cat] : '#7c3aed';
  }

  private addRadiusLayers(): void {
    if (this.map.getSource(this.RING_SOURCE)) return;
    const c = this.map.getCenter();
    this.map.addSource(this.RING_SOURCE, {
      type: 'geojson',
      data: this.metersToCircle(c.lng, c.lat, this.selectedRadius()),
    });
    const color = this.ringColor();
    this.map.addLayer({
      id: 'search-radius-fill',
      type: 'fill',
      source: this.RING_SOURCE,
      paint: { 'fill-color': color, 'fill-opacity': 0.07 },
    });
    this.map.addLayer({
      id: 'search-radius-glow',
      type: 'line',
      source: this.RING_SOURCE,
      paint: { 'line-color': color, 'line-width': 10, 'line-opacity': 0.18, 'line-blur': 6 },
    });
    this.map.addLayer({
      id: 'search-radius-line',
      type: 'line',
      source: this.RING_SOURCE,
      paint: { 'line-color': color, 'line-width': 1.5, 'line-opacity': 0.9, 'line-dasharray': [2, 2] },
    });
    this.ringReady = true;
  }

  private updateRadiusRing(): void {
    if (!this.ringReady) return;
    const c = this.map.getCenter();
    const src = this.map.getSource(this.RING_SOURCE) as maplibregl.GeoJSONSource | undefined;
    src?.setData(this.metersToCircle(c.lng, c.lat, this.selectedRadius()));
    const color = this.ringColor();
    this.map.setPaintProperty('search-radius-fill', 'fill-color', color);
    this.map.setPaintProperty('search-radius-glow', 'line-color', color);
    this.map.setPaintProperty('search-radius-line', 'line-color', color);
  }

  // A slow, subtle breathing of the outer glow — the "live radar" feel. Honors
  // reduced-motion preferences.
  private startRingPulse(): void {
    const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    if (reduce || !this.ringReady) return;
    const tick = () => {
      const t = (Math.sin(performance.now() / 1600) + 1) / 2; // 0..1, ~3.2s period
      if (this.map.getLayer('search-radius-glow')) {
        this.map.setPaintProperty('search-radius-glow', 'line-opacity', 0.12 + t * 0.22);
      }
      this.pulseFrame = requestAnimationFrame(tick);
    };
    this.pulseFrame = requestAnimationFrame(tick);
  }

  centerOnUser(): void {
    const pos = this.geoService.position();
    if (pos) {
      this.map.flyTo({ center: [pos.lng, pos.lat], zoom: 14, duration: 1200 });
    } else {
      this.geoService.requestLocation().then(p =>
        this.map.flyTo({ center: [p.lng, p.lat], zoom: 14, duration: 1200 }),
      );
    }
  }

  flyTo(lng: number, lat: number): void {
    this.map.flyTo({ center: [lng, lat], zoom: 15, duration: 1400 });
  }

  ngOnDestroy(): void {
    if (this.pulseFrame !== null) cancelAnimationFrame(this.pulseFrame);
    this.map?.remove();
  }
}
