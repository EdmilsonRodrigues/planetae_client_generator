
import { HttpClient, HttpParams } from '@angular/common/http'
import { environment } from '@env/environment'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import * as models from '../models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.APIHost}/api/client/contents`

  constructor (private http: HttpClient) { }

  signIn(request: models.BodySignIn): Observable<models.AuthResponse> {
    return this.http.post<models.AuthResponse>(`${this.apiUrl}/api/client/auth/sign-in`, request)
  }

  signUp(): Observable<models.BaseAuthResponse> {
    return this.http.post<models.BaseAuthResponse>(`${this.apiUrl}/api/client/auth/sign-up`)
  }

  signInWithToken(): Observable<models.BaseAuthResponse> {
    return this.http.post<models.BaseAuthResponse>(`${this.apiUrl}/api/client/auth/sign-in-with-token`)
  }

  loginWithOutseta(request: models.Credentials): Observable<models.OutsetaLoginResponse> {
    return this.http.post<models.OutsetaLoginResponse>(`${this.apiUrl}/api/client/auth/login-with-outseta`, request)
  }

  resetPassword(username: string): Observable<models.ActionModel> {
    return this.http.get<models.ActionModel>(`${this.apiUrl}/api/client/auth/reset-password/${username}`)
  }
}