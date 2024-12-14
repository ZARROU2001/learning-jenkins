import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TokenStorageService {

  private currentUserSubject: BehaviorSubject<any | null>;
  public currentUser$: Observable<any | null>;
  private USER_KEY = 'auth-user';

  constructor() {
    let storageUser: any | null = null;
    const storageUserAsStr = sessionStorage.getItem(this.USER_KEY);
    if (storageUserAsStr) {
      storageUser = JSON.parse(storageUserAsStr);
    }
    this.currentUserSubject = new BehaviorSubject<any | null>(storageUser);
    this.currentUser$ = this.currentUserSubject.asObservable();
  }

  signOut(): void {
    if (this.getUser() != null) {
      window.sessionStorage.clear();
      this.currentUserSubject.next(null);
    }
  }

  public saveUser(user: any): void {
    window.sessionStorage.setItem(this.USER_KEY, JSON.stringify(user));
    this.currentUserSubject.next(user);
  }

  public isLoggedIn() {
    if (window.sessionStorage.getItem(this.USER_KEY) !== null) {
      return true;
    }
    return false;

  }

  public getUser(): any {
    const user = window.sessionStorage.getItem(this.USER_KEY);
    if (user) {
      return JSON.parse(user);
    }
    return null;
  }
}
