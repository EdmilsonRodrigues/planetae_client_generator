
import { HttpClient, HttpParams } from '@angular/common/http'
import { environment } from '@env/environment'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import * as models from '../models';

@Injectable({
  providedIn: 'root'
})
export class InfringementsService {
  private apiUrl = `${environment.APIHost}/api/client/contents`

  constructor (private http: HttpClient) { }

  listInfringement(filters: string, page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/infringements/?filters=${filters}&page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  createInfringement(request: models.InfringementRequest): Observable<models.Infringement> {
    return this.http.post<models.Infringement>(`${this.apiUrl}/api/client/infringements/`, request)
  }

  getInfringementsCount(): Observable<models.CountInfringements> {
    return this.http.get<models.CountInfringements>(`${this.apiUrl}/api/client/infringements/count`)
  }

  readInfringement(infringement_id: string): Observable<models.Infringement> {
    return this.http.get<models.Infringement>(`${this.apiUrl}/api/client/infringements/${infringement_id}`)
  }

  whitelistInfringement(level: models.Level, infringement_id: string): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/infringements/${infringement_id}/whitelist/${level}`)
  }

  unwhitelistInfringement(level: models.Level, infringement_id: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/infringements/${infringement_id}/whitelist/${level}`)
  }

  getInfringementsFrames(infringement_id: string): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiUrl}/api/client/infringements/${infringement_id}/frames`)
  }

  getInfringementFrame(frame_path: string, infringement_id: string): Observable<null> {
    return this.http.get<null>(`${this.apiUrl}/api/client/infringements/${infringement_id}/frames/${frame_path}`)
  }

  takedownInfringement(infringement_id: string): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/infringements/${infringement_id}/takedown`)
  }

  verifyInfringement(infringement_id: string, request: models.BodyVerifyInfringement): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/infringements/${infringement_id}/verify`, request)
  }
}