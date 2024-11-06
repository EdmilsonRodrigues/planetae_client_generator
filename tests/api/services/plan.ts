
import { HttpClient, HttpParams } from '@angular/common/http'
import { environment } from '@env/environment'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import * as models from '../models';

@Injectable({
  providedIn: 'root'
})
export class PlanService {
  private apiUrl = `${environment.APIHost}/api/client/contents`

  constructor (private http: HttpClient) { }

  updateSubscriptionPlans (request: models.UpdateSubscriptionData): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/api/client/plan/update`, request)
  }
}