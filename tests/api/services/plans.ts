
import { HttpClient, HttpParams } from '@angular/common/http'
import { environment } from '@env/environment'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import * as models from '../models';

@Injectable({
  providedIn: 'root'
})
export class PlansService {
  private apiUrl = `${environment.APIHost}/api/client/contents`

  constructor (private http: HttpClient) { }

  listPlans(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/plans`)
  }
}