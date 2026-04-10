import { CommonModule } from '@angular/common';
import { Component, computed } from '@angular/core';
import { Router } from '@angular/router';

import { SearchHistoryEntry } from '../../core/models/job.model';
import { UserDataService } from '../../core/services/user-data.service';

@Component({
  selector: 'app-activity-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './activity-page.component.html',
  styleUrl: './activity-page.component.css'
})
export class ActivityPageComponent {
  readonly history = computed(() => this.userData.searchHistory());
  readonly totalResultsReviewed = computed(() =>
    this.userData.searchHistory().reduce((sum, item) => sum + item.resultsCount, 0)
  );
  readonly topCountries = computed(() => {
    const countryCounts = this.userData.searchHistory().reduce<Record<string, number>>(
      (counts, item) => ({
        ...counts,
        [item.country]: (counts[item.country] ?? 0) + 1
      }),
      {}
    );

    return Object.entries(countryCounts).sort((a, b) => b[1] - a[1]).slice(0, 3);
  });

  constructor(
    private readonly router: Router,
    protected readonly userData: UserDataService
  ) {}

  runAgain(entry: SearchHistoryEntry) {
    void this.router.navigate(['/search'], {
      queryParams: {
        query: entry.query,
        country: entry.country,
        location: entry.location || null,
        distance: entry.distance !== null ? String(entry.distance) : null,
        page: entry.page,
        work_mode: entry.workMode || null,
        type: entry.type || null
      }
    });
  }

  trackByHistory(_index: number, entry: SearchHistoryEntry) {
    return entry.id;
  }
}
