import { Injectable, computed, signal } from '@angular/core';

import {
  Job,
  SavedJob,
  SearchHistoryEntry,
  JobSearchFilters
} from '../models/job.model';

@Injectable({ providedIn: 'root' })
export class UserDataService {
  private readonly savedJobsKey = 'jobsearch.saved-jobs.v1';
  private readonly searchHistoryKey = 'jobsearch.search-history.v1';

  readonly savedJobs = signal<SavedJob[]>(this.readStored<SavedJob[]>(this.savedJobsKey, []));
  readonly searchHistory = signal<SearchHistoryEntry[]>(
    this.readStored<SearchHistoryEntry[]>(this.searchHistoryKey, [])
  );

  readonly savedCount = computed(() => this.savedJobs().length);
  readonly noteCount = computed(
    () => this.savedJobs().filter((job) => job.note.trim().length > 0).length
  );
  readonly remoteSavedCount = computed(
    () => this.savedJobs().filter((job) => job.remote).length
  );

  saveJob(job: Job) {
    const existing = this.getSavedJob(job.id);

    if (existing) {
      return existing;
    }

    const savedJob: SavedJob = {
      ...job,
      savedAt: new Date().toISOString(),
      note: ''
    };

    this.savedJobs.set([savedJob, ...this.savedJobs()]);
    this.persist(this.savedJobsKey, this.savedJobs());

    return savedJob;
  }

  toggleSaved(job: Job) {
    if (this.isSaved(job.id)) {
      this.removeSavedJob(job.id);
      return;
    }

    this.saveJob(job);
  }

  removeSavedJob(jobId: string) {
    this.savedJobs.set(this.savedJobs().filter((job) => job.id !== jobId));
    this.persist(this.savedJobsKey, this.savedJobs());
  }

  updateNote(jobId: string, note: string, sourceJob?: Job) {
    if (!this.isSaved(jobId) && sourceJob) {
      this.saveJob(sourceJob);
    }

    this.savedJobs.set(
      this.savedJobs().map((job) =>
        job.id === jobId
          ? {
              ...job,
              note
            }
          : job
      )
    );

    this.persist(this.savedJobsKey, this.savedJobs());
  }

  addSearchHistory(filters: JobSearchFilters, resultsCount: number) {
    const entry: SearchHistoryEntry = {
      id: this.createId(),
      query: filters.query,
      country: filters.country,
      location: filters.location,
      distance: filters.distance,
      page: filters.page,
      workMode: filters.workMode,
      type: filters.type,
      resultsCount,
      searchedAt: new Date().toISOString()
    };

    const dedupedEntries = this.searchHistory().filter(
      (historyItem) =>
        !(
          historyItem.query === entry.query &&
          historyItem.country === entry.country &&
          historyItem.location === entry.location &&
          historyItem.distance === entry.distance &&
          historyItem.page === entry.page &&
          historyItem.workMode === entry.workMode &&
          historyItem.type === entry.type
        )
    );

    this.searchHistory.set([entry, ...dedupedEntries].slice(0, 12));
    this.persist(this.searchHistoryKey, this.searchHistory());
  }

  isSaved(jobId: string): boolean {
    return this.savedJobs().some((job) => job.id === jobId);
  }

  getSavedJob(jobId: string): SavedJob | undefined {
    return this.savedJobs().find((job) => job.id === jobId);
  }

  private createId(): string {
    return typeof crypto !== 'undefined' && 'randomUUID' in crypto
      ? crypto.randomUUID()
      : `${Date.now()}-${Math.random().toString(36).slice(2)}`;
  }

  private persist(key: string, value: SavedJob[] | SearchHistoryEntry[]) {
    localStorage.setItem(key, JSON.stringify(value));
  }

  private readStored<T>(key: string, fallback: T): T {
    const storedValue = localStorage.getItem(key);

    if (!storedValue) {
      return fallback;
    }

    try {
      return JSON.parse(storedValue) as T;
    } catch {
      localStorage.removeItem(key);
      return fallback;
    }
  }
}
