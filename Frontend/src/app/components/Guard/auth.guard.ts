import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router); // Inject the Router
  const accessToken = localStorage.getItem('access_token'); // Check if the user has an access token

  if (accessToken) {
    // If the user is already authenticated, redirect to the dashboard
    router.navigate(['/']);
    return false; // Prevent access to the login route
  }

  // Allow access to the login route if no access token is found
  return true;
};
