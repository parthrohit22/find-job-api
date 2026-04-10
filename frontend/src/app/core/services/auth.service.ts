import { Injectable, computed, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, map, tap } from 'rxjs';

import { AuthResponse, UserSession } from '../models/job.model';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly storageKey = 'jobsearch.session.v1';
  private readonly sessionState = signal<UserSession | null>(this.readSession());

  readonly session = computed(() => this.sessionState());
  readonly isAuthenticated = computed(() => this.sessionState() !== null);
  readonly displayName = computed(() => this.sessionState()?.name ?? 'Guest');

  constructor(
    private readonly http: HttpClient,
    private readonly router: Router
  ) {}

  register(name: string, email: string, password: string): Observable<UserSession> {
    return this.http
      .post<AuthResponse>('/api/auth/register', {
        name: name.trim(),
        email: email.trim(),
        password
      })
      .pipe(
        map((response) => this.toSession(response)),
        tap((session) => this.persistSession(session))
      );
  }

  login(email: string, password: string): Observable<UserSession> {
    return this.http
      .post<AuthResponse>('/api/auth/login', {
        email: email.trim(),
        password
      })
      .pipe(
        map((response) => this.toSession(response)),
        tap((session) => this.persistSession(session))
      );
  }

  logout() {
    this.sessionState.set(null);
    localStorage.removeItem(this.storageKey);
    void this.router.navigate(['/login']);
  }

  private persistSession(session: UserSession) {
    this.sessionState.set(session);
    localStorage.setItem(this.storageKey, JSON.stringify(session));
  }

  private toSession(response: AuthResponse): UserSession {
    return {
      name: response.user.name,
      email: response.user.email,
      apiKey: response.apiKey,
      keyPreview: response.user.keyPreview,
      loggedInAt: new Date().toISOString()
    };
  }

  private readSession(): UserSession | null {
    const rawSession = localStorage.getItem(this.storageKey);

    if (!rawSession) {
      return null;
    }

    try {
      return JSON.parse(rawSession) as UserSession;
    } catch {
      localStorage.removeItem(this.storageKey);
      return null;
    }
  }
}
