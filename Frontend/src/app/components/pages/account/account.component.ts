import { Component } from '@angular/core';
import { CustomizerSettingsService } from '../../customizer-settings/customizer-settings.service';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormBuilder, FormGroup, Validators,ReactiveFormsModule } from '@angular/forms'; // Importation pour les formulaires réactifs
import { NgIf, CommonModule } from '@angular/common'; // Import de CommonModule et NgIf

@Component({
    selector: 'app-account',
    standalone: true,
    imports: [RouterLink, MatCardModule, MatButtonModule, MatMenuModule, RouterLinkActive, MatFormFieldModule, MatInputModule,NgIf,CommonModule,ReactiveFormsModule],
    templateUrl: './account.component.html',
    styleUrls: ['./account.component.scss']
})
export class AccountComponent {
    UpdateForm: FormGroup;

    constructor(
        public themeService: CustomizerSettingsService,
        private fb: FormBuilder
    ) {
        {
            this.UpdateForm = this.fb.group({
                firstName: ['', Validators.required],
                lastName: ['', Validators.required],
                username: ['', Validators.required],
                email: ['', [Validators.required, Validators.email]],
            })
        }
    }

    onSubmit(): void {
        if (this.UpdateForm.valid) {
          const formData = {
            email: this.UpdateForm.value.email,
            first_name: this.UpdateForm.value.firstName,
            last_name: this.UpdateForm.value.lastName,
            username: this.UpdateForm.value.username,
          };
          console.log(formData)
        } else {
          console.log('Form is invalid');
        }
      }

    isFieldInvalid(field: string): boolean {
        const control = this.UpdateForm.get(field);
        const formErrors = this.UpdateForm.errors;
        return (control?.invalid && (control.dirty || control.touched)) || (formErrors && formErrors['passwordsMismatch'] && field === 'confirmPassword');
    }
    toggleTheme() {
        this.themeService.toggleTheme();
    }

    toggleRTLEnabledTheme() {
        this.themeService.toggleRTLEnabledTheme();
    }

}