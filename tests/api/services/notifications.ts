
import { HttpClient, HttpParams } from '@angular/common/http'
import { environment } from '@env/environment'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import * as models from '../models';

@Injectable({
  providedIn: 'root'
})
export class NotificationsService {
  private apiUrl = `${environment.APIHost}/api/client/contents`

  constructor (private http: HttpClient) { }

  readNotifications (page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<models.PaginatedResults> {
    return this.http.get<models.PaginatedResults>(`${this.apiUrl}/api/client/notifications/?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }
}