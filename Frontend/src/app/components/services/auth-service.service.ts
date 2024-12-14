import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthServiceService {
   private authUrl = "http://127.0.0.1:8000/api/v1/users/signup";
   private authUrl2 = "http://localhost:8001/auth/login";

  constructor(private http : HttpClient) { }

  register(signUp: any): Observable<object> {
    return this.http.post(this.authUrl, signUp);
  }
  login(loginData: { email: string; password: string }): Observable<object> {
    return this.http.post(this.authUrl2, loginData);
  }

}
