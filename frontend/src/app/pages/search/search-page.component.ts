import { CommonModule } from '@angular/common';
import { Component, OnInit, computed, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { finalize } from 'rxjs';

import {
  Job,
  JobSearchFilters,
  SearchHistoryEntry
} from '../../core/models/job.model';
import { JobApiService } from '../../core/services/job-api.service';
import { UserDataService } from '../../core/services/user-data.service';

@Component({
  selector: 'app-search-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './search-page.component.html',
  styleUrl: './search-page.component.css'
})
export class SearchPageComponent implements OnInit {
  private readonly api = inject(JobApiService);
  private readonly formBuilder = inject(FormBuilder);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  protected readonly userData = inject(UserDataService);

  readonly form = this.formBuilder.group({
    query: ['software engineer'],
    country: ['us'],
    location: [''],
    distance: [null as number | null],
    page: [1],
    workMode: [''],
    type: ['']
  });

  readonly history = computed(() => this.userData.searchHistory().slice(0, 5));
  readonly suggestions = computed(() =>
    Array.from(new Set(this.userData.searchHistory().map((item) => item.query))).slice(0, 6)
  );
  readonly savedCount = computed(() => this.userData.savedCount());
  readonly response = this.api.lastResponse;

  loading = false;
  errorMessage = '';

  ngOnInit() {
    this.hydrateFromRouteOrCache();
  }

  search(syncUrl = true) {
    const filters = this.getFilters();

    if (!filters.query.trim()) {
      this.errorMessage = 'Enter a search query to load jobs.';
      return;
    }

    if (syncUrl) {
      void this.router.navigate([], {
        relativeTo: this.route,
        queryParams: this.toQueryParams(filters)
      });
    }

    this.loading = true;
    this.errorMessage = '';

    this.api
      .searchJobs(filters)
      .pipe(finalize(() => (this.loading = false)))
      .subscribe({
        next: (response) => {
          this.userData.addSearchHistory(filters, response.count);
        },
        error: (error: { error?: { error?: string; details?: string } }) => {
          this.errorMessage =
            error.error?.details ??
            error.error?.error ??
            'Unable to load jobs right now. Check the backend credentials and try again.';
        }
      });
  }

  applyHistory(entry: SearchHistoryEntry) {
    this.form.patchValue({
      query: entry.query,
      country: entry.country,
      location: entry.location ?? '',
      distance: entry.distance ?? null,
      page: entry.page,
      workMode: entry.workMode ?? '',
      type: entry.type
    });

    this.search();
  }

  useSuggestion(query: string) {
    this.form.patchValue({ query, page: 1 });
    this.search();
  }

  toggleSaved(job: Job) {
    this.userData.toggleSaved(job);
  }

  isSaved(jobId: string): boolean {
    return this.userData.isSaved(jobId);
  }

  clearFilters() {
    this.form.reset({
      query: '',
      country: 'us',
      location: '',
      distance: null,
      page: 1,
      workMode: '',
      type: ''
    });

    this.errorMessage = '';
    this.api.lastFilters.set(null);
    this.api.lastResponse.set(null);
    void this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {}
    });
  }

  trackByJob(_index: number, job: Job) {
    return job.id;
  }

  modeLabel(mode: string | null | undefined) {
    const normalized = (mode || '').toLowerCase();
    if (!normalized) {
      return 'Flexible';
    }

    return normalized.charAt(0).toUpperCase() + normalized.slice(1);
  }

  private hydrateFromRouteOrCache() {
    const queryParams = this.route.snapshot.queryParamMap;
    const query = queryParams.get('query');

    if (query) {
      this.form.patchValue({
        query,
        country: queryParams.get('country') ?? 'us',
        location: queryParams.get('location') ?? '',
        distance: queryParams.get('distance') ? Number(queryParams.get('distance')) : null,
        page: Number(queryParams.get('page') ?? 1),
        workMode: queryParams.get('work_mode') ?? '',
        type: queryParams.get('type') ?? ''
      });

      this.search(false);
      return;
    }

    const cachedFilters = this.api.lastFilters();

    if (cachedFilters) {
      this.form.patchValue({
        query: cachedFilters.query,
        country: cachedFilters.country,
        location: cachedFilters.location,
        distance: cachedFilters.distance,
        page: cachedFilters.page,
        workMode: cachedFilters.workMode,
        type: cachedFilters.type
      });
      return;
    }

    const latestSearch = this.userData.searchHistory()[0];

    if (latestSearch) {
      this.form.patchValue({
        query: latestSearch.query,
        country: latestSearch.country,
        location: latestSearch.location ?? '',
        distance: latestSearch.distance ?? null,
        page: latestSearch.page,
        workMode: latestSearch.workMode ?? '',
        type: latestSearch.type
      });
    }
  }

  private getFilters(): JobSearchFilters {
    const rawValue = this.form.getRawValue();

    return {
      query: (rawValue.query ?? '').trim(),
      country: (rawValue.country ?? 'us').trim(),
      location: (rawValue.location ?? '').trim(),
      distance: rawValue.distance === null || rawValue.distance === undefined
        ? null
        : Number(rawValue.distance),
      page: Math.max(1, Number(rawValue.page ?? 1) || 1),
      workMode: (rawValue.workMode ?? '').trim(),
      type: (rawValue.type ?? '').trim()
    };
  }

  private toQueryParams(filters: JobSearchFilters) {
    return {
      query: filters.query.trim(),
      country: filters.country.trim().toLowerCase() || 'us',
      location: filters.location.trim() || null,
      distance: filters.distance !== null ? String(filters.distance) : null,
      page: Math.max(1, Number(filters.page) || 1),
      work_mode: filters.workMode.trim().toLowerCase() || null,
      type: filters.type.trim().toUpperCase() || null
    };
  }
}
