import { HttpClient, HttpParams } from '@angular/common/http'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import { environment, PaginatedResponse } from '@env/environment'

export class Content {
  id: string
  title: string
  type: string
  description: string
  modelName: string
  urls: string[]
  imagePreview: string
  infringementPreferences: InfringementPreferences
  files: string[]
  detectionStrings: string[]
  allowedDomains: string[]
  is_verified: boolean
  owner: string
}
  

export interface InfringementPreferences {
  
}
  
  
@Injectable({
  providedIn: 'root'
})
export class ContentService {
  private apiUrl = `${environment.APIHost}/api/client/contents`

  constructor (private http: HttpClient) { }

}