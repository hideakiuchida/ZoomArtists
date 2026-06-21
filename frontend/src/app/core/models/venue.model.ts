import { Coordinates } from './event.model';

export interface VenueResponse {
  id: string;
  name: string;
  address: string;
  city: string;
  country: string;
  coordinates: Coordinates;
  google_maps_url: string | null;
  capacity: number | null;
  description: string | null;
  accessibility: string[];
  transit_info: string[];
}
