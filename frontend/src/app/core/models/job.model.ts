export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  remote: boolean;
  work_mode: string | null;
  distance_km: number | null;
  employment_type: string | null;
  apply_link: string | null;
  apply_source: string | null;
  apply_type: string | null;
}

export interface JobSearchFilters {
  query: string;
  country: string;
  location: string;
  distance: number | null;
  page: number;
  workMode: string;
  type: string;
}

export interface JobSearchResponse {
  cached: boolean;
  query: string;
  country: string;
  source: string;
  warning: string | null;
  filters: {
    location: string;
    distance: number | null;
    work_mode: string;
    type: string;
  };
  page: number;
  count: number;
  results: Job[];
}

export interface SavedJob extends Job {
  savedAt: string;
  note: string;
}

export interface SearchHistoryEntry {
  id: string;
  query: string;
  country: string;
  location: string;
  distance: number | null;
  page: number;
  workMode: string;
  type: string;
  resultsCount: number;
  searchedAt: string;
}

export interface UserSession {
  name: string;
  email: string;
  apiKey: string;
  keyPreview: string;
  loggedInAt: string;
}

export interface AuthResponse {
  message: string;
  apiKey: string;
  user: {
    name: string;
    email: string;
    keyPreview: string;
  };
}
