
import { HttpClient, HttpParams } from '@angular/common/http'
import { environment } from '@env/environment'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import * as models from '../models';

@Injectable({
  providedIn: 'root'
})
export class PersonService {
  private apiUrl = `${environment.APIHost}/api/client/contents`

  constructor (private http: HttpClient) { }

  readPersonsMe(): Observable<models.Person> {
    return this.http.get<models.Person>(`${this.apiUrl}/api/client/person/me`)
  }

  updatePersonsMe(): Observable<models.Person> {
    return this.http.patch<models.Person>(`${this.apiUrl}/api/client/person/me`)
  }

  updateInfringementPreferences(request: models.FastapiCompatBodyUpdateInfringementPreferences2): Observable<models.Person> {
    return this.http.patch<models.Person>(`${this.apiUrl}/api/client/person/me/infringement-preferences`, request)
  }

  readPerson(person_id: string): Observable<models.Person> {
    return this.http.get<models.Person>(`${this.apiUrl}/api/client/person/${person_id}`)
  }
}