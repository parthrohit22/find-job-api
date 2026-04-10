import { Injectable, signal } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

import { Job, JobSearchFilters, JobSearchResponse } from '../models/job.model';

@Injectable({ providedIn: 'root' })
export class JobApiService {
  readonly lastResponse = signal<JobSearchResponse | null>(null);
  readonly lastFilters = signal<JobSearchFilters | null>(null);

  constructor(private readonly http: HttpClient) {}

  searchJobs(filters: JobSearchFilters): Observable<JobSearchResponse> {
    const normalizedFilters = this.normalizeFilters(filters);

    let params = new HttpParams()
      .set('query', normalizedFilters.query)
      .set('country', normalizedFilters.country)
      .set('page', String(normalizedFilters.page));

    if (normalizedFilters.location) {
      params = params.set('location', normalizedFilters.location);
    }

    if (normalizedFilters.distance !== null) {
      params = params.set('distance', String(normalizedFilters.distance));
    }

    if (normalizedFilters.workMode) {
      params = params.set('work_mode', normalizedFilters.workMode);
    }

    if (normalizedFilters.type) {
      params = params.set('type', normalizedFilters.type);
    }

    return this.http
      .get<JobSearchResponse>('/api/jobs', { params })
      .pipe(
        tap((response) => {
          this.lastFilters.set(normalizedFilters);
          this.lastResponse.set(response);
        })
      );
  }

  findJobById(jobId: string): Job | undefined {
    return this.lastResponse()?.results.find((job) => job.id === jobId);
  }

  private normalizeFilters(filters: JobSearchFilters): JobSearchFilters {
    return {
      query: filters.query.trim(),
      country: filters.country.trim().toLowerCase() || 'us',
      location: filters.location.trim(),
      distance: filters.distance === null || filters.distance === undefined
        ? null
        : Math.max(0, Number(filters.distance) || 0),
      page: Math.max(1, Number(filters.page) || 1),
      workMode: filters.workMode.trim().toLowerCase(),
      type: filters.type.trim().toUpperCase()
    };
  }
}
