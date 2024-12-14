import { Component } from '@angular/core';
import { CustomizerSettingsService } from '../../customizer-settings/customizer-settings.service';
import { RouterLink } from '@angular/router';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { NgIf, CommonModule } from '@angular/common'; // Import de CommonModule et NgIf
import { FormBuilder, FormGroup, Validators,ReactiveFormsModule } from '@angular/forms'; // Importation pour les formulaires réactifs

@Component({
    selector: 'app-reset-password',
    standalone: true,
    imports: [RouterLink, MatFormFieldModule, MatInputModule, MatIconModule, MatButtonModule,NgIf,CommonModule,ReactiveFormsModule],
    templateUrl: './reset-password.component.html',
    styleUrls: ['./reset-password.component.scss']
})
export class ResetPasswordComponent {

    hide = true;
    resetPasForm: FormGroup;

    constructor(
        public themeService: CustomizerSettingsService,
        private fb: FormBuilder,
    ) {
        {
            this.resetPasForm = this.fb.group({
            password: ['', [Validators.required, Validators.minLength(6)]],
            confirmPassword: ['', Validators.required],
            }, 
             { validator: this.passwordsMatchValidator 

            }); 
        }

    }

    onSubmit(): void {
        if (this.resetPasForm.valid) {
          const formData = {
            password: this.resetPasForm.value.password,
          };
          console.log(formData)

        } else {
          console.log('Password is invalid');
        }
      }

    passwordsMatchValidator(resetPasForm: FormGroup): { [key: string]: boolean } | null {
        const password = resetPasForm.get('password')?.value;
        const confirmPassword = resetPasForm.get('confirmPassword')?.value;
        if (password && confirmPassword && password !== confirmPassword) {
            return { passwordsMismatch: true };
        }
        return null;
    }

    // Vérifier si les champs du formulaire sont valides
    isFieldInvalid(field: string): boolean {
        const control = this.resetPasForm.get(field);
        const formErrors = this.resetPasForm.errors;
        return (control?.invalid && (control.dirty || control.touched)) || (formErrors && formErrors['passwordsMismatch'] && field === 'confirmPassword');
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