import { Component } from '@angular/core';
import { CustomizerSettingsService } from '../../customizer-settings/customizer-settings.service';
import {  Router, RouterLink } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { FormBuilder, FormGroup, Validators,ReactiveFormsModule } from '@angular/forms'; // Importation pour les formulaires réactifs
import { NgIf, CommonModule } from '@angular/common'; // Import de CommonModule et NgIf
import { AuthServiceService } from '../../services/auth-service.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
    selector: 'app-register',
    standalone: true,
    imports: [
        RouterLink,
        MatButtonModule,
        MatFormFieldModule,
        MatInputModule,
        MatIconModule,
        NgIf,CommonModule,
        ReactiveFormsModule],
    templateUrl: './register.component.html',
    styleUrls: ['./register.component.scss']
})
export class RegisterComponent {

    hide = true;
    registerForm: FormGroup;
    horizontalPosition: 'start' | 'center' | 'end' = 'end';
    verticalPosition: 'top' | 'bottom' = 'top';


    constructor(
        
        public themeService: CustomizerSettingsService,
        private fb: FormBuilder,
        public authService: AuthServiceService,
        private router:Router,
        private snackBar: MatSnackBar
    ) {
        {
            this.registerForm = this.fb.group({
                firstName: ['', Validators.required],
                lastName: ['', Validators.required],
                username: ['', Validators.required],
                email: ['', [Validators.required, Validators.email]],
                password: ['', [Validators.required, Validators.minLength(6)]],
                confirmPassword: ['', Validators.required],
            }, { validator: this.passwordsMatchValidator });
            
        }
    }


    onSubmit(): void {
        if (this.registerForm.valid) {
          const formData = {
            email: this.registerForm.value.email,
            first_name: this.registerForm.value.firstName,
            last_name: this.registerForm.value.lastName,
            password: this.registerForm.value.password,
            username: this.registerForm.value.username,
          };
          console.log(formData)
    
          this.authService.register(formData).subscribe({
            next: (response) => {
              console.log('User registered successfully', response);
              this.router.navigate(['/authentication/login']); 
            },
            error: (error) => {
              console.error('Error registering user', error);
            },
          });
        } else {
          console.log('Form is invalid');
        }
      }
    
    // Vérifier si les champs du formulaire sont valides
    isFieldInvalid(field: string): boolean {
        const control = this.registerForm.get(field);
        const formErrors = this.registerForm.errors;
        return (control?.invalid && (control.dirty || control.touched)) || (formErrors && formErrors['passwordsMismatch'] && field === 'confirmPassword');
    }
    

    passwordsMatchValidator(form: FormGroup): { [key: string]: boolean } | null {
        const password = form.get('password')?.value;
        const confirmPassword = form.get('confirmPassword')?.value;
        if (password && confirmPassword && password !== confirmPassword) {
            return { passwordsMismatch: true };
        }
        return null;
    }

    openSnackBar(message: string, action: string): void {
        this.snackBar.open(message, action, {
          horizontalPosition: this.horizontalPosition,
          verticalPosition: this.verticalPosition,
          duration: 3000,
        });
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