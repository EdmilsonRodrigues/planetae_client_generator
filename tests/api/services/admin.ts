
import { HttpClient, HttpParams } from '@angular/common/http'
import { environment } from '@env/environment'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import * as models from '../models';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private apiUrl = `${environment.APIHost}/api/client/contents`

  constructor (private http: HttpClient) { }

  adminListPersons(page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/persons/?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  adminCreatePerson(request: models.Person): Observable<models.Person> {
    return this.http.post<models.Person>(`${this.apiUrl}/api/client/admin/persons/`, request)
  }

  adminReadPerson(person_id: string): Observable<models.Person> {
    return this.http.get<models.Person>(`${this.apiUrl}/api/client/admin/persons/${person_id}`)
  }

  adminUpdatePerson(person_id: string, request: models.Person): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/api/client/admin/persons/${person_id}`, request)
  }

  adminDeletePerson(person_id: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/admin/persons/${person_id}`)
  }

  adminImpersonatePerson(person_id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/persons/${person_id}/impersonate`)
  }

  adminListSubscriptions(page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/subscriptions?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  adminCreateSubscription(request: models.Subscription): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/api/client/admin/subscriptions`, request)
  }

  adminListPlans(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/plans`)
  }

  adminUpdateSubscriptionPlans(request: models.UpdateSubscriptionData): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/api/client/admin/plan/update`, request)
  }

  adminReadSubscription(subscription_id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/subscriptions/${subscription_id}`)
  }

  adminUpdateSubscription(subscription_id: string, request: models.Subscription): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/api/client/admin/subscriptions/${subscription_id}`, request)
  }

  adminDeleteSubscription(subscription_id: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/admin/subscriptions/${subscription_id}`)
  }

  adminListInfringements(page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/infringements/?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  adminCreateInfringement(request: models.Infringement): Observable<models.Infringement> {
    return this.http.post<models.Infringement>(`${this.apiUrl}/api/client/admin/infringements/`, request)
  }

  adminGetPotentialVaInfringements(): Observable<models.PotentialVAResponse> {
    return this.http.get<models.PotentialVAResponse>(`${this.apiUrl}/api/client/admin/infringements/potential`)
  }

  adminReadInfringement(infringement_id: string): Observable<models.Infringement> {
    return this.http.get<models.Infringement>(`${this.apiUrl}/api/client/admin/infringements/${infringement_id}`)
  }

  adminUpdateInfringement(infringement_id: string, request: models.Infringement): Observable<models.Infringement> {
    return this.http.put<models.Infringement>(`${this.apiUrl}/api/client/admin/infringements/${infringement_id}`, request)
  }

  adminDeleteInfringement(infringement_id: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/admin/infringements/${infringement_id}`)
  }

  adminGetInfringementsFrames(infringement_id: string): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiUrl}/api/client/admin/infringements/${infringement_id}/frames`)
  }

  adminGetInfringementFrame(frame_path: string, infringement_id: string): Observable<null> {
    return this.http.get<null>(`${this.apiUrl}/api/client/admin/infringements/${infringement_id}/frames/${frame_path}`)
  }

  adminTakedownInfringement(infringement_id: string): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/admin/infringements/${infringement_id}/takedown`)
  }

  adminVerifyInfringement(infringement_id: string, request: models.BodyAdminVerifyInfringement): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/admin/infringements/${infringement_id}/verify`, request)
  }

  adminAutomaticallyVerifyInfringement(infringement_id: string, request: models.BodyAdminAutomaticallyVerifyInfringement): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/admin/infringements/${infringement_id}/automatic-verify`, request)
  }

  adminListInfrastructure(page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/infrastructure?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  adminListTasks(page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/tasks?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  adminListPendingTasks(): Observable<models.PendingTasks[]> {
    return this.http.get<models.PendingTasks[]>(`${this.apiUrl}/api/client/admin/tasks-pending`)
  }

  adminReadInfrastructure(infrastructure_id: string): Observable<models.Infrastructure> {
    return this.http.get<models.Infrastructure>(`${this.apiUrl}/api/client/admin/infrastructure/${infrastructure_id}`)
  }

  adminDeleteInfrastructure(infrastructure_id: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/admin/infrastructure/${infrastructure_id}`)
  }

  adminListContents(page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/contents/?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  adminCreateContent(request: models.Content): Observable<models.Content> {
    return this.http.post<models.Content>(`${this.apiUrl}/api/client/admin/contents/`, request)
  }

  adminReadContent(content_id: string): Observable<models.Content> {
    return this.http.get<models.Content>(`${this.apiUrl}/api/client/admin/contents/${content_id}`)
  }

  adminUpdateContent(content_id: string, request: models.Content): Observable<models.Content> {
    return this.http.put<models.Content>(`${this.apiUrl}/api/client/admin/contents/${content_id}`, request)
  }

  adminDeleteContent(content_id: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/admin/contents/${content_id}`)
  }

  adminAddContentDetectionStrings(content_id: string, request: models.BodyAdminAddContentDetectionStrings): Observable<models.Content> {
    return this.http.post<models.Content>(`${this.apiUrl}/api/client/admin/contents/${content_id}/detection_string`, request)
  }

  adminDeleteContentDetectionStrings(detectionString: string, content_id: string): Observable<models.Content> {
    return this.http.delete<models.Content>(`${this.apiUrl}/api/client/admin/contents/${content_id}/detection_string/${detectionString}`)
  }

  adminAddContentAllowedDomains(content_id: string, request: models.BodyAdminAddContentAllowedDomains): Observable<models.Content> {
    return this.http.post<models.Content>(`${this.apiUrl}/api/client/admin/contents/${content_id}/allowed_domain`, request)
  }

  adminDeleteContentAllowedDomains(allowedDomain: string, content_id: string): Observable<models.Content> {
    return this.http.delete<models.Content>(`${this.apiUrl}/api/client/admin/contents/${content_id}/allowed_domain/${allowedDomain}`)
  }

  adminBatchUpdateContent(action_type: models.ActionTypes, request: string[]): Observable<models.ActionModel> {
    return this.http.put<models.ActionModel>(`${this.apiUrl}/api/client/admin/contents/action/${action_type}`, request)
  }

  adminGetContentFile(content_id: string, file_name: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/contents/uploads/${content_id}/${file_name}`)
  }

  adminDeleteFile(file_name: string, content_id: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/admin/contents/${content_id}/files/${file_name}`)
  }

  adminUploadContentFiles(content_id: string, request: models.BodyAdminUploadContentFiles): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/admin/contents/${content_id}/files`, request)
  }

  adminGetVideos(task_id: string | null, url: string | null, title: string | null, description: string | null, tags: string[] | null, duration: string | null, views: string | null, likes: string | null, dislikes: string | null, favorites: string | null, rating: string | null, uploader_url: string | null, uploader: string | null, uploader_verified: boolean | null, uploader_producer: boolean | null, categories: string[] | null, comments: string[] | null, num_comments: number | null, video_length: number | null, video_file: string | null, created_at: string | null, page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/videos/?task_id=${task_id}&url=${url}&title=${title}&description=${description}&tags=${tags}&duration=${duration}&views=${views}&likes=${likes}&dislikes=${dislikes}&favorites=${favorites}&rating=${rating}&uploader_url=${uploader_url}&uploader=${uploader}&uploader_verified=${uploader_verified}&uploader_producer=${uploader_producer}&categories=${categories}&comments=${comments}&num_comments=${num_comments}&video_length=${video_length}&video_file=${video_file}&created_at=${created_at}&page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }
}