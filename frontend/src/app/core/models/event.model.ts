export type EventCategory =
  | 'music' | 'visual_art' | 'theater' | 'dance'
  | 'spoken_word' | 'cinema' | 'festival' | 'workshop' | 'street_performance';

export type EventStatus = 'draft' | 'pending' | 'published' | 'cancelled' | 'past';

export interface Coordinates {
  longitude: number;
  latitude: number;
}

export interface EventSummary {
  id: string;
  title: string;
  category: EventCategory;
  status: EventStatus;
  start_date: string;
  cover_image: string | null;
  is_free: boolean;
  ticket_price: number | null;
  currency: string;
  coordinates: Coordinates;
  distance_meters: number | null;
  venue_name: string;
  artist_names: string[];
}

export interface EventResponse {
  id: string;
  title: string;
  description: string | null;
  category: EventCategory;
  status: EventStatus;
  start_date: string;
  end_date: string | null;
  cover_image: string | null;
  gallery: string[];
  video_url: string | null;
  ticket_url: string | null;
  ticket_price: number | null;
  currency: string;
  is_free: boolean;
  capacity: number | null;
  tags: string[];
  coordinates: Coordinates;
  distance_meters: number | null;
  venue: VenueResponse;
  artists: ArtistSummary[];
  organizer_id: string;
  created_at: string;
  updated_at: string;
}

export interface NearbyEventsResponse {
  events: EventSummary[];
  total: number;
  next_cursor: string | null;
}

export interface NearbyEventsQuery {
  lat: number;
  lng: number;
  radius?: number;
  category?: EventCategory;
  is_free?: boolean;
  limit?: number;
  cursor?: string;
}

// Imported here to avoid circular imports in small model file
import { ArtistSummary } from './artist.model';
import { VenueResponse } from './venue.model';

export const CATEGORY_COLORS: Record<EventCategory, string> = {
  music: '#7c3aed',
  visual_art: '#f59e0b',
  theater: '#ec4899',
  dance: '#f97316',
  spoken_word: '#10b981',
  cinema: '#3b82f6',
  festival: '#ef4444',
  workshop: '#06b6d4',
  street_performance: '#84cc16',
};

export const CATEGORY_LABELS: Record<EventCategory, string> = {
  music: 'Música',
  visual_art: 'Arte Visual',
  theater: 'Teatro',
  dance: 'Danza',
  spoken_word: 'Spoken Word',
  cinema: 'Cine',
  festival: 'Festival',
  workshop: 'Taller',
  street_performance: 'Performance Callejero',
};

export const CATEGORY_ICONS: Record<EventCategory, string> = {
  music: '🎵',
  visual_art: '🎨',
  theater: '🎭',
  dance: '💃',
  spoken_word: '🎤',
  cinema: '🎬',
  festival: '🎉',
  workshop: '🛠️',
  street_performance: '🎪',
};
