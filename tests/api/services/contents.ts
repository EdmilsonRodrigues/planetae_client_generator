
import { HttpClient, HttpParams } from '@angular/common/http'
import { environment } from '@env/environment'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import * as models from '../models';

@Injectable({
  providedIn: 'root'
})
export class ContentsService {
  private apiUrl = `${environment.APIHost}`

  constructor (private http: HttpClient) { }

  listContent (page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/contents/?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  createContent (request: models.ContentRequest): Observable<models.Content> {
    return this.http.post<models.Content>(`${this.apiUrl}/api/client/contents/`, request)
  }

  listContentByAccounid (page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = '', accountId: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/contents/byteam/${accountId}?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  readContent (contentId: string): Observable<models.Content> {
    return this.http.get<models.Content>(`${this.apiUrl}/api/client/contents/${contentId}`)
  }

  updateContent (contentId: string, request: models.Content): Observable<models.Content> {
    return this.http.put<models.Content>(`${this.apiUrl}/api/client/contents/${contentId}`, request)
  }

  deleteContent (contentId: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/contents/${contentId}`)
  }

  addContentDetectionStrings (contentId: string, request: models.BodyAddContentDetectionStrings): Observable<models.Content> {
    return this.http.post<models.Content>(`${this.apiUrl}/api/client/contents/${contentId}/detection_string`, request)
  }

  deleteContentDetectionStrings (detectionString: string, contentId: string): Observable<models.Content> {
    return this.http.delete<models.Content>(`${this.apiUrl}/api/client/contents/${contentId}/detection_string/${detectionString}`)
  }

  addContentAllowedDomains (contentId: string, request: models.BodyAddContentAllowedDomains): Observable<models.Content> {
    return this.http.post<models.Content>(`${this.apiUrl}/api/client/contents/${contentId}/allowed_domain`, request)
  }

  deleteContentAllowedDomains (allowedDomain: string, contentId: string): Observable<models.Content> {
    return this.http.delete<models.Content>(`${this.apiUrl}/api/client/contents/${contentId}/allowed_domain/${allowedDomain}`)
  }

  updateInfringementPreferences (contentId: string, request: models.FastapiCompatBodyUpdateInfringementPreferences1): Observable<models.ActionModel> {
    return this.http.patch<models.ActionModel>(`${this.apiUrl}/api/client/contents/${contentId}/infringement-preferences`, request)
  }

  uploadContentFiles (contentId: string, request: models.BodyUploadContentFiles): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/contents/${contentId}/files`, request)
  }

  getContentFile (contentId: string, fileName: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/contents/uploads/${contentId}/${fileName}`)
  }

  deleteFile (fileName: string, contentId: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/contents/${contentId}/files/${fileName}`)
  }
}