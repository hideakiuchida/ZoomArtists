export interface SocialLinks {
  instagram?: string;
  spotify?: string;
  soundcloud?: string;
  youtube?: string;
  website?: string;
}

export interface ArtistSummary {
  id: string;
  name: string;
  profile_image: string | null;
  genres: string[];
  category: string;
}

export interface ArtistResponse {
  id: string;
  name: string;
  slug: string;
  bio: string | null;
  category: string;
  genres: string[];
  profile_image: string | null;
  gallery: string[];
  audio_preview_url: string | null;
  social_links: SocialLinks | null;
  is_verified: boolean;
  verified_at: string | null;
  follower_count: number;
}
