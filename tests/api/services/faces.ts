
import { HttpClient, HttpParams } from '@angular/common/http'
import { environment } from '@env/environment'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import * as models from '../models';

@Injectable({
  providedIn: 'root'
})
export class FacesService {
  private apiUrl = `${environment.APIHost}/api/client/contents`

  constructor (private http: HttpClient) { }

  readFaces (page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<models.PaginatedResults> {
    return this.http.get<models.PaginatedResults>(`${this.apiUrl}/api/client/faces/?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  readUnknownFaces (page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<models.PaginatedResults> {
    return this.http.get<models.PaginatedResults>(`${this.apiUrl}/api/client/faces/unknown?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  readFace (faceId: string): Observable<models.Face> {
    return this.http.get<models.Face>(`${this.apiUrl}/api/client/faces/${faceId}`)
  }

  getFaceImage (faceId: string): Observable<null> {
    return this.http.get<null>(`${this.apiUrl}/api/client/faces/face/${faceId}/images`)
  }
}