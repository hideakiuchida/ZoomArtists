import { Injectable, signal } from '@angular/core';

export interface GeoPosition {
  lat: number;
  lng: number;
}

@Injectable({ providedIn: 'root' })
export class GeolocationService {
  position = signal<GeoPosition | null>(null);
  error = signal<string | null>(null);

  // Default: Mexico City
  private readonly DEFAULT: GeoPosition = { lat: 19.4326, lng: -99.1332 };

  requestLocation(): Promise<GeoPosition> {
    return new Promise((resolve) => {
      if (!navigator.geolocation) {
        this.position.set(this.DEFAULT);
        resolve(this.DEFAULT);
        return;
      }
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const coords = { lat: pos.coords.latitude, lng: pos.coords.longitude };
          this.position.set(coords);
          resolve(coords);
        },
        () => {
          this.error.set('No se pudo obtener tu ubicación. Mostrando ubicación por defecto.');
          this.position.set(this.DEFAULT);
          resolve(this.DEFAULT);
        },
        { timeout: 8000 },
      );
    });
  }
}
