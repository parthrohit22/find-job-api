import { CommonModule } from '@angular/common';
import { Component, computed } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

import { AuthService } from '../core/services/auth.service';
import { UserDataService } from '../core/services/user-data.service';

@Component({
  selector: 'app-shell-layout',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive, RouterOutlet],
  templateUrl: './shell-layout.component.html',
  styleUrl: './shell-layout.component.css'
})
export class ShellLayoutComponent {
  readonly savedCount = computed(() => this.userData.savedCount());
  readonly searchCount = computed(() => this.userData.searchHistory().length);

  constructor(
    protected readonly auth: AuthService,
    private readonly userData: UserDataService
  ) {}

  logout() {
    this.auth.logout();
  }
}
