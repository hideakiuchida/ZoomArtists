export type UserRole = 'attendee' | 'artist' | 'organizer' | 'admin';

export interface User {
  id: string;
  email: string;
  name: string;
  avatar: string | null;
  role: UserRole;
  notifications_enabled: boolean;
  saved_event_ids: string[];
  followed_artist_ids: string[];
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}
