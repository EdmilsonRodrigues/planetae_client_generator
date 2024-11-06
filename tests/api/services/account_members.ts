
import { HttpClient, HttpParams } from '@angular/common/http'
import { environment } from '@env/environment'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import * as models from '../models';

@Injectable({
  providedIn: 'root'
})
export class Account_MembersService {
  private apiUrl = `${environment.APIHost}/api/client/contents`

  constructor (private http: HttpClient) { }

  listAccountMember(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/account_members`)
  }

  createAccountMember(request: models.AccountMemberInvite): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/api/client/account_members`, request)
  }

  readAccountMember(account_member_id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/account_members/${account_member_id}`)
  }

  defaultUpdateAccountMember(account_member_id: string, request: models.AccountMemberInvite): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/api/client/account_members/${account_member_id}`, request)
  }

  deleteAccountMember(account_member_id: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/api/client/account_members/${account_member_id}`)
  }
}