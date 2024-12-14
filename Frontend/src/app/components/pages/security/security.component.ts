import { Component } from '@angular/core';
import { CustomizerSettingsService } from '../../customizer-settings/customizer-settings.service';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { NgIf, CommonModule } from '@angular/common'; // Import de CommonModule et NgIf
import { FormBuilder, FormGroup, Validators,ReactiveFormsModule } from '@angular/forms'; // Importation pour les formulaires réactifs

@Component({
    selector: 'app-security',
    standalone: true,
    imports: [RouterLink, MatCardModule, MatButtonModule, MatMenuModule, RouterLinkActive, MatFormFieldModule, MatInputModule, MatIconModule, MatCheckboxModule, NgIf,CommonModule, ReactiveFormsModule],
    templateUrl: './security.component.html',
    styleUrls: ['./security.component.scss']
})
export class SecurityComponent {

    hide = true;
    updatePassForm: FormGroup;
    constructor(
        public themeService: CustomizerSettingsService,
        private fb: FormBuilder,

    ) {
        {
            this.updatePassForm = this.fb.group({
                password: ['', [Validators.required, Validators.minLength(6)]],
                confirmPassword: ['', Validators.required],
            }, { validator: this.passwordsMatchValidator });
            
        }
    }

    onSubmit(): void {
        if (this.updatePassForm.valid) {
          const formData = {
            password: this.updatePassForm.value.password,
          };
          console.log(formData)
        } else {
          console.log('Form is invalid');
        }
      }

    // Vérifier si les champs du formulaire sont valides
    isFieldInvalid(field: string): boolean {
        const control = this.updatePassForm.get(field);
        const formErrors = this.updatePassForm.errors;
        return (control?.invalid && (control.dirty || control.touched)) || (formErrors && formErrors['passwordsMismatch'] && field === 'confirmPassword');
    }
    passwordsMatchValidator(updatePassForm: FormGroup): { [key: string]: boolean } | null {
        const password = updatePassForm.get('password')?.value;
        const confirmPassword = updatePassForm.get('confirmPassword')?.value;
        if (password && confirmPassword && password !== confirmPassword) {
            return { passwordsMismatch: true };
        }
        return null;
    }
    toggleTheme() {
        this.themeService.toggleTheme();
    }

    toggleRTLEnabledTheme() {
        this.themeService.toggleRTLEnabledTheme();
    }

}