import { CommonModule } from '@angular/common';
import { Component, computed, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { SavedJob } from '../../core/models/job.model';
import { UserDataService } from '../../core/services/user-data.service';

@Component({
  selector: 'app-saved-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './saved-page.component.html',
  styleUrl: './saved-page.component.css'
})
export class SavedPageComponent {
  readonly query = signal('');
  readonly filteredJobs = computed(() => {
    const term = this.query().trim().toLowerCase();

    if (!term) {
      return this.userData.savedJobs();
    }

    return this.userData.savedJobs().filter((job) =>
      [job.title, job.company, job.location, job.note]
        .join(' ')
        .toLowerCase()
        .includes(term)
    );
  });

  constructor(protected readonly userData: UserDataService) {}

  setQuery(value: string) {
    this.query.set(value);
  }

  updateNote(job: SavedJob, note: string) {
    this.userData.updateNote(job.id, note, job);
  }

  remove(jobId: string) {
    this.userData.removeSavedJob(jobId);
  }

  trackBySaved(_index: number, job: SavedJob) {
    return job.id;
  }
}
