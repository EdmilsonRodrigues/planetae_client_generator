
import { HttpClient, HttpParams } from '@angular/common/http'
import { environment } from '@env/environment'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import * as models from '../models';

@Injectable({
  providedIn: 'root'
})
export class ContentsService {
  private apiUrl = `${environment.APIHost}/api/client/contents`

  constructor (private http: HttpClient) { }

  listContent(page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/contents/?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  createContent(request: models.ContentRequest): Observable<models.Content> {
    return this.http.post<models.Content>(`${this.apiUrl}/api/client/contents/`, request)
  }

  listContentByAccounid(page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = '', account_id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/contents/byteam/${account_id}?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  readContent(content_id: string): Observable<models.Content> {
    return this.http.get<models.Content>(`${this.apiUrl}/api/client/contents/${content_id}`)
  }

  updateContent(content_id: string, request: models.Content): Observable<models.Content> {
    return this.http.put<models.Content>(`${this.apiUrl}/api/client/contents/${content_id}`, request)
  }

  deleteContent(content_id: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/contents/${content_id}`)
  }

  addContentDetectionStrings(content_id: string, request: models.BodyAddContentDetectionStrings): Observable<models.Content> {
    return this.http.post<models.Content>(`${this.apiUrl}/api/client/contents/${content_id}/detection_string`, request)
  }

  deleteContentDetectionStrings(detectionString: string, content_id: string): Observable<models.Content> {
    return this.http.delete<models.Content>(`${this.apiUrl}/api/client/contents/${content_id}/detection_string/${detectionString}`)
  }

  addContentAllowedDomains(content_id: string, request: models.BodyAddContentAllowedDomains): Observable<models.Content> {
    return this.http.post<models.Content>(`${this.apiUrl}/api/client/contents/${content_id}/allowed_domain`, request)
  }

  deleteContentAllowedDomains(allowedDomain: string, content_id: string): Observable<models.Content> {
    return this.http.delete<models.Content>(`${this.apiUrl}/api/client/contents/${content_id}/allowed_domain/${allowedDomain}`)
  }

  updateInfringementPreferences(content_id: string, request: models.FastapiCompatBodyUpdateInfringementPreferences1): Observable<models.ActionModel> {
    return this.http.patch<models.ActionModel>(`${this.apiUrl}/api/client/contents/${content_id}/infringement-preferences`, request)
  }

  uploadContentFiles(content_id: string, request: models.BodyUploadContentFiles): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/contents/${content_id}/files`, request)
  }

  getContentFile(content_id: string, file_name: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/contents/uploads/${content_id}/${file_name}`)
  }

  deleteFile(file_name: string, content_id: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/contents/${content_id}/files/${file_name}`)
  }
}