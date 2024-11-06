
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

  adminListPersons (page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/persons/?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  adminCreatePerson (request: models.Person): Observable<models.Person> {
    return this.http.post<models.Person>(`${this.apiUrl}/api/client/admin/persons/`, request)
  }

  adminReadPerson (personId: string): Observable<models.Person> {
    return this.http.get<models.Person>(`${this.apiUrl}/api/client/admin/persons/${personId}`)
  }

  adminUpdatePerson (personId: string, request: models.Person): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/api/client/admin/persons/${personId}`, request)
  }

  adminDeletePerson (personId: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/admin/persons/${personId}`)
  }

  adminImpersonatePerson (personId: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/persons/${personId}/impersonate`)
  }

  adminListSubscriptions (page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/subscriptions?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  adminCreateSubscription (request: models.Subscription): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/api/client/admin/subscriptions`, request)
  }

  adminListPlans (): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/plans`)
  }

  adminUpdateSubscriptionPlans (request: models.UpdateSubscriptionData): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/api/client/admin/plan/update`, request)
  }

  adminReadSubscription (subscriptionId: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/subscriptions/${subscriptionId}`)
  }

  adminUpdateSubscription (subscriptionId: string, request: models.Subscription): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/api/client/admin/subscriptions/${subscriptionId}`, request)
  }

  adminDeleteSubscription (subscriptionId: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/admin/subscriptions/${subscriptionId}`)
  }

  adminListInfringements (page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/infringements/?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  adminCreateInfringement (request: models.Infringement): Observable<models.Infringement> {
    return this.http.post<models.Infringement>(`${this.apiUrl}/api/client/admin/infringements/`, request)
  }

  adminGetPotentialVaInfringements (): Observable<models.PotentialVAResponse> {
    return this.http.get<models.PotentialVAResponse>(`${this.apiUrl}/api/client/admin/infringements/potential`)
  }

  adminReadInfringement (infringementId: string): Observable<models.Infringement> {
    return this.http.get<models.Infringement>(`${this.apiUrl}/api/client/admin/infringements/${infringementId}`)
  }

  adminUpdateInfringement (infringementId: string, request: models.Infringement): Observable<models.Infringement> {
    return this.http.put<models.Infringement>(`${this.apiUrl}/api/client/admin/infringements/${infringementId}`, request)
  }

  adminDeleteInfringement (infringementId: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/admin/infringements/${infringementId}`)
  }

  adminGetInfringementsFrames (infringementId: string): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiUrl}/api/client/admin/infringements/${infringementId}/frames`)
  }

  adminGetInfringementFrame (framePath: string, infringementId: string): Observable<null> {
    return this.http.get<null>(`${this.apiUrl}/api/client/admin/infringements/${infringementId}/frames/${framePath}`)
  }

  adminTakedownInfringement (infringementId: string): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/admin/infringements/${infringementId}/takedown`)
  }

  adminVerifyInfringement (infringementId: string, request: models.BodyAdminVerifyInfringement): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/admin/infringements/${infringementId}/verify`, request)
  }

  adminAutomaticallyVerifyInfringement (infringementId: string, request: models.BodyAdminAutomaticallyVerifyInfringement): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/admin/infringements/${infringementId}/automatic-verify`, request)
  }

  adminListInfrastructure (page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/infrastructure?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  adminListTasks (page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/tasks?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  adminListPendingTasks (): Observable<models.PendingTasks[]> {
    return this.http.get<models.PendingTasks[]>(`${this.apiUrl}/api/client/admin/tasks-pending`)
  }

  adminReadInfrastructure (infrastructureId: string): Observable<models.Infrastructure> {
    return this.http.get<models.Infrastructure>(`${this.apiUrl}/api/client/admin/infrastructure/${infrastructureId}`)
  }

  adminDeleteInfrastructure (infrastructureId: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/admin/infrastructure/${infrastructureId}`)
  }

  adminListContents (page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/contents/?page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }

  adminCreateContent (request: models.Content): Observable<models.Content> {
    return this.http.post<models.Content>(`${this.apiUrl}/api/client/admin/contents/`, request)
  }

  adminReadContent (contentId: string): Observable<models.Content> {
    return this.http.get<models.Content>(`${this.apiUrl}/api/client/admin/contents/${contentId}`)
  }

  adminUpdateContent (contentId: string, request: models.Content): Observable<models.Content> {
    return this.http.put<models.Content>(`${this.apiUrl}/api/client/admin/contents/${contentId}`, request)
  }

  adminDeleteContent (contentId: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/admin/contents/${contentId}`)
  }

  adminAddContentDetectionStrings (contentId: string, request: models.BodyAdminAddContentDetectionStrings): Observable<models.Content> {
    return this.http.post<models.Content>(`${this.apiUrl}/api/client/admin/contents/${contentId}/detection_string`, request)
  }

  adminDeleteContentDetectionStrings (detectionString: string, contentId: string): Observable<models.Content> {
    return this.http.delete<models.Content>(`${this.apiUrl}/api/client/admin/contents/${contentId}/detection_string/${detectionString}`)
  }

  adminAddContentAllowedDomains (contentId: string, request: models.BodyAdminAddContentAllowedDomains): Observable<models.Content> {
    return this.http.post<models.Content>(`${this.apiUrl}/api/client/admin/contents/${contentId}/allowed_domain`, request)
  }

  adminDeleteContentAllowedDomains (allowedDomain: string, contentId: string): Observable<models.Content> {
    return this.http.delete<models.Content>(`${this.apiUrl}/api/client/admin/contents/${contentId}/allowed_domain/${allowedDomain}`)
  }

  adminBatchUpdateContent (actionType: models.ActionTypes, request: string[]): Observable<models.ActionModel> {
    return this.http.put<models.ActionModel>(`${this.apiUrl}/api/client/admin/contents/action/${actionType}`, request)
  }

  adminGetContentFile (contentId: string, fileName: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/contents/uploads/${contentId}/${fileName}`)
  }

  adminDeleteFile (fileName: string, contentId: string): Observable<models.ActionModel> {
    return this.http.delete<models.ActionModel>(`${this.apiUrl}/api/client/admin/contents/${contentId}/files/${fileName}`)
  }

  adminUploadContentFiles (contentId: string, request: models.BodyAdminUploadContentFiles): Observable<models.ActionModel> {
    return this.http.post<models.ActionModel>(`${this.apiUrl}/api/client/admin/contents/${contentId}/files`, request)
  }

  adminGetVideos (taskId: string | null, url: string | null, title: string | null, description: string | null, tags: string[] | null, duration: string | null, views: string | null, likes: string | null, dislikes: string | null, favorites: string | null, rating: string | null, uploaderUrl: string | null, uploader: string | null, uploaderVerified: boolean | null, uploaderProducer: boolean | null, categories: string[] | null, comments: string[] | null, numComments: number | null, videoLength: number | null, videoFile: string | null, createdAt: string | null, page: number = 0, size: number = 10, sort: string = '_id', order: string = 'asc', search: string | null = ''): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/client/admin/videos/?taskId=${taskId}&url=${url}&title=${title}&description=${description}&tags=${tags}&duration=${duration}&views=${views}&likes=${likes}&dislikes=${dislikes}&favorites=${favorites}&rating=${rating}&uploaderUrl=${uploaderUrl}&uploader=${uploader}&uploaderVerified=${uploaderVerified}&uploaderProducer=${uploaderProducer}&categories=${categories}&comments=${comments}&numComments=${numComments}&videoLength=${videoLength}&videoFile=${videoFile}&createdAt=${createdAt}&page=${page}&size=${size}&sort=${sort}&order=${order}&search=${search}`)
  }
}