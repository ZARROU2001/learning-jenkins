import { Component } from '@angular/core';
import { CustomizerSettingsService } from '../../customizer-settings/customizer-settings.service';
import { RouterLink } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { NgIf,CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
    selector: 'app-forgot-password',
    standalone: true,
    imports: [RouterLink, MatButtonModule, MatFormFieldModule, MatInputModule,CommonModule,NgIf,ReactiveFormsModule],
    templateUrl: './forgot-password.component.html',
    styleUrls: ['./forgot-password.component.scss']
})
export class ForgotPasswordComponent {
    FogotPasForm: FormGroup;
    constructor(
        public themeService: CustomizerSettingsService,
        private fb: FormBuilder
    ) {
        this.FogotPasForm = this.fb.group({
            email: ['', [Validators.required, Validators.email]],
        });
    }

    isFieldInvalid(field: string): boolean {
        const control = this.FogotPasForm.get(field);
        return control ? control.invalid && control.touched : false;
    }
    onSubmit(): void {
        if (this.FogotPasForm.valid) {
          console.log('Form Submitted', this.FogotPasForm.value);
          // Call your login API here
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