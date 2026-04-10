import { CommonModule } from '@angular/common';
import { Component, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { Job } from '../../core/models/job.model';
import { JobApiService } from '../../core/services/job-api.service';
import { UserDataService } from '../../core/services/user-data.service';

@Component({
  selector: 'app-job-detail-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './job-detail-page.component.html',
  styleUrl: './job-detail-page.component.css'
})
export class JobDetailPageComponent implements OnInit {
  readonly job = signal<Job | null>(null);

  constructor(
    private readonly route: ActivatedRoute,
    private readonly api: JobApiService,
    protected readonly userData: UserDataService
  ) {}

  ngOnInit() {
    const jobId = this.route.snapshot.paramMap.get('id');

    if (!jobId) {
      return;
    }

    this.job.set(this.userData.getSavedJob(jobId) ?? this.api.findJobById(jobId) ?? null);
  }

  isSaved(jobId: string) {
    return this.userData.isSaved(jobId);
  }

  toggleSaved(job: Job) {
    this.userData.toggleSaved(job);
  }

  updateNote(job: Job, note: string) {
    this.userData.updateNote(job.id, note, job);
  }
}
