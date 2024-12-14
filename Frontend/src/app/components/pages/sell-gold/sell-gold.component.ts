import { Component } from '@angular/core';
import { CustomizerSettingsService } from '../../customizer-settings/customizer-settings.service';
import { FormsModule, NgModel } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card'; // Voir Problème 2

@Component({
  selector: 'app-sell-gold',
  standalone: true,
  imports: [CommonModule,FormsModule,MatCardModule],
  templateUrl: './sell-gold.component.html',
  styleUrl: './sell-gold.component.scss'
})
export class SellGoldComponent {
  walletBalance: string = '$12,426.07';
    currencies: string[] = ['BTC', 'ETH', 'LTC', 'CDR'];
    selectedCurrency: string = 'BTC';
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
    this.total = this.amount - this.transactionFee;
  }

  onSell(): void {
    this.calculateTotal();
    console.log('Selling:', this.amount, this.selectedCurrency);
  }
}
