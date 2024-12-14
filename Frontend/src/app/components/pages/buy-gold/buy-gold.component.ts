import { Component } from '@angular/core';
import { CustomizerSettingsService } from '../../customizer-settings/customizer-settings.service';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { ReactiveFormsModule } from '@angular/forms'; // Importation pour les formulaires réactifs
import { NgIf, CommonModule } from '@angular/common'; // Import de CommonModule et NgIf
import { NgModel } from '@angular/forms';
import { FormsModule } from '@angular/forms'; // Importer FormsModule

@Component({
  selector: 'app-buy-gold',
  standalone: true,
  imports: [ReactiveFormsModule,CommonModule,FormsModule,MatCardModule],
  templateUrl: './buy-gold.component.html',
  styleUrl: './buy-gold.component.scss'
})
export class BuyGoldComponent {
  walletBalance: string = '$12,426.07';
    currencies: string[] = ['BTC', 'ETH', 'LTC', 'CDR'];
    selectedCurrency: string = 'BTC';
    paymentMethod: string = '';
    amount: number = 0;
    estimatedRate: string = '1 BTC ~ $34,572.00';
    transactionFeePercentage: number = 0.05;
    transactionFee: number = 0;
    total: number = 0;

  constructor(
    public themeService: CustomizerSettingsService
) {}

  calculateTotal(): void {
    this.transactionFee = (this.amount * this.transactionFeePercentage) / 100;
    this.total = this.amount + this.transactionFee;
}

onBuy(): void {
  this.calculateTotal();
  console.log('Buying:', this.amount, this.selectedCurrency);
}
}
