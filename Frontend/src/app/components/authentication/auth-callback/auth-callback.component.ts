import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TokenStorageService } from '../../services/token-storage.service';

@Component({
  selector: 'app-auth-callback',
  standalone: true,
  imports: [],
  templateUrl: './auth-callback.component.html',
  styleUrl: './auth-callback.component.scss'
})
export class AuthCallbackComponent {


  constructor(private route: ActivatedRoute, private router : Router, private tokenStorage: TokenStorageService) { }



  ngOnInit(): void {
    // Get the token from the URL parameters
    this.route.queryParams.subscribe(params => {
      const accessToken = params['access_token'];
      const refreshToken = params['refresh_token'];

      if (accessToken && refreshToken) {
        // Store the tokens securely in localStorage
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);

        // Redirect to the dashboard or wherever you'd like
        this.router.navigate(['']); // Adjust to your app's main route
      } else {
        // Handle missing tokens
        console.error('Tokens are missing in the URL');
      }
    });
  }

}
