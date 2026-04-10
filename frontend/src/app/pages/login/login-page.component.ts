import { HttpErrorResponse } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { finalize } from 'rxjs';

import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login-page.component.html',
  styleUrl: './login-page.component.css'
})
export class LoginPageComponent implements OnInit {
  private readonly auth = inject(AuthService);
  private readonly formBuilder = inject(FormBuilder);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  readonly authMode = signal<'register' | 'signin'>('register');
  readonly form = this.formBuilder.nonNullable.group({
    name: ['Parth Rohit', [Validators.required, Validators.minLength(2)]],
    email: ['parth@example.com', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
    confirmPassword: ['', [Validators.required]]
  });

  submitting = false;
  errorMessage = '';

  ngOnInit() {
    this.applyModeValidators();

    if (this.auth.isAuthenticated()) {
      void this.router.navigate(['/search']);
    }
  }

  setMode(mode: 'register' | 'signin') {
    this.authMode.set(mode);
    this.errorMessage = '';
    this.applyModeValidators();
  }

  submit() {
    if (this.form.invalid || this.submitting) {
      this.form.markAllAsTouched();
      return;
    }

    const { name, email, password, confirmPassword } = this.form.getRawValue();
    const redirectTo = this.route.snapshot.queryParamMap.get('redirectTo') || '/search';

    if (this.authMode() === 'register' && password !== confirmPassword) {
      this.errorMessage = 'Confirm password must match the password field.';
      return;
    }

    this.submitting = true;
    this.errorMessage = '';

    const request$ = this.authMode() === 'register'
      ? this.auth.register(name, email, password)
      : this.auth.login(email, password);

    request$
      .pipe(finalize(() => (this.submitting = false)))
      .subscribe({
        next: () => {
          void this.router.navigateByUrl(redirectTo);
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage = this.getErrorMessage(error);
        }
      });
  }

  private getErrorMessage(error: HttpErrorResponse): string {
    if (error.status === 0) {
      return 'Frontend cannot reach the Flask API. Start the backend on port 5001 and start Angular with "npm start" so the proxy is enabled.';
    }

    if (error.status === 400 || error.status === 401 || error.status === 409) {
      return error.error?.error ?? 'Please check the form details and try again.';
    }

    if (error.status === 404) {
      return 'Auth routes were not found. Restart both Flask and Angular so the latest API is loaded.';
    }

    if (error.status >= 500) {
      return 'The backend responded with a server error. Check the Flask terminal for details.';
    }

    return error.error?.error ?? 'Authentication failed. Check your details and try again.';
  }

  private applyModeValidators() {
    const nameControl = this.form.controls.name;
    const confirmPasswordControl = this.form.controls.confirmPassword;

    if (this.authMode() === 'register') {
      nameControl.setValidators([Validators.required, Validators.minLength(2)]);
      confirmPasswordControl.setValidators([Validators.required]);
    } else {
      nameControl.clearValidators();
      confirmPasswordControl.clearValidators();
    }

    nameControl.updateValueAndValidity({ emitEvent: false });
    confirmPasswordControl.updateValueAndValidity({ emitEvent: false });
  }
}
