
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

  readInfringement(infringementId: string): Observable<models.Infringement> {
    return this.http.get<models.Infringement>(`${this.apiUrl}/api/client/infringements/${{infringementId}}`)
  }

  whitelistInfringement(level: models.Level, infringementId: string): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/infringements/${{infringementId}}/whitelist/${{level}}`)
  }

  unwhitelistInfringement(level: models.Level, infringementId: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/infringements/${{infringementId}}/whitelist/${{level}}`)
  }

  getInfringementsFrames(infringementId: string): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiUrl}/api/client/infringements/${{infringementId}}/frames`)
  }

  getInfringementFrame(framePath: string, infringementId: string): Observable<null> {
    return this.http.get<null>(`${this.apiUrl}/api/client/infringements/${{infringementId}}/frames/${{framePath}}`)
  }

  takedownInfringement(infringementId: string): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/infringements/${{infringementId}}/takedown`)
  }

  verifyInfringement(infringementId: string, request: models.BodyVerifyInfringement): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/infringements/${{infringementId}}/verify`, request)
  }
}