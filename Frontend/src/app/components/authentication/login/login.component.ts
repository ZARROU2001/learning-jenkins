import { Component } from '@angular/core';
import { CustomizerSettingsService } from '../../customizer-settings/customizer-settings.service';
import { Router, RouterLink } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { NgIf,CommonModule } from '@angular/common';
import { AuthServiceService } from '../../services/auth-service.service';
CommonModule
@Component({
    selector: 'app-login',
    standalone: true,
    imports: [RouterLink, MatButtonModule, MatFormFieldModule, MatInputModule, MatIconModule, MatCheckboxModule,CommonModule,NgIf,ReactiveFormsModule],
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss']
})
export class LoginComponent {
    loginForm: FormGroup;
    hide = true;

    constructor(
        public themeService: CustomizerSettingsService,
        private fb: FormBuilder,
        private authService : AuthServiceService,
        private router:Router,


    ) {
        this.loginForm = this.fb.group({
            email: ['', [Validators.required, Validators.email]],
            password: ['', [Validators.required, Validators.minLength(6)]],
        });
    }

    isFieldInvalid(field: string): boolean {
        const control = this.loginForm.get(field);
        return control ? control.invalid && control.touched : false;
    }

    onSubmit(): void {
        if (this.loginForm.valid) {
          console.log('Form Submitted', this.loginForm.value);
          this.authService.login(this.loginForm.value).subscribe({
            next: (response:any) => {
              console.log('Login Successful', response);
              // Stocker les jetons dans localStorage
              localStorage.setItem('access_token', response.access_token);
              localStorage.setItem('refresh_token', response.refresh_token);
      
              // Rediriger l'utilisateur vers le dashboard après connexion réussie
              this.router.navigate(['/dashboard']);
            },
            error: (err) => {
              console.error('Login Failed', err);
              // Afficher une erreur à l'utilisateur
            }
          });
        } else {
          console.warn('Form is invalid');
        }
      }
      
    toggleTheme() {
        this.themeService.toggleTheme();
    }

    toggleCardBorderTheme() {
        this.themeService.toggleCardBorderTheme();
    }

    toggleCardBorderRadiusTheme() {
        this.themeService.toggleCardBorderRadiusTheme();
    }

    toggleRTLEnabledTheme() {
        this.themeService.toggleRTLEnabledTheme();
    }

}