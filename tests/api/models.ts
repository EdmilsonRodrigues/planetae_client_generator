export interface AccountMemberInvite {
	createdAt: Date
	updatedAt: Date
	_id?: string
	accountId: string
	subscriptionId: string
	name: string
	username: string
	firstName?: string
	lastName?: string
	email: string
	role?: UserRoles
	seats?: number
	plan_type?: string
	accountStageLabel?: string
	createdBy: string
}

export interface ActionModel {
	action: string
	message: string
	status: string
	detail: string
}

export interface ActionTypes {
}

export interface AuthResponse {
	access_token: string
	refresh_token: string
	token_type?: string
	person: string
}

export interface BaseAuthResponse {
	access_token: string
	refresh_token: string
	token_type?: string
}

export interface BodyAddContentAllowedDomains {
	allowedDomain: string
}

export interface BodyAddContentDetectionStrings {
	detectionString: string
}

export interface BodyAdminAddContentAllowedDomains {
	allowedDomain: string
}

export interface BodyAdminAddContentDetectionStrings {
	detectionString: string
}

export interface BodyAdminAutomaticallyVerifyInfringement {
	verify: boolean
}

export interface BodyAdminUploadContentFiles {
	files: string[]
}

export interface BodyAdminVerifyInfringement {
	verified: boolean
}

export interface BodySignIn {
	grant_type: string | null
	username: string
	password: string
	scope?: string
	client_id: string | null
	client_secret: string | null
}

export interface BodyUploadContentFiles {
	files: string[]
}

export interface BodyVerifyInfringement {
	verified: boolean
}

export interface Content {
	createdAt: Date
	updatedAt: Date
	title: string
	type: ContentTypes
	modelName: string
	description: string
	urls?: string[]
	detectionStrings?: string[]
	_id?: string
	face_id: string | null
	metadata?: any
	owner: string
	accountId?: string
	imagePreview?: string
	infringementPreferences?: InfringementPreferences
	allowedDomains?: string[]
	files?: string[]
	is_verified?: boolean
}

export interface ContentRequest {
	createdAt: Date
	updatedAt: Date
	title: string
	type: ContentTypes
	modelName: string
	description: string
	urls?: string[]
	detectionStrings?: string[]
}

export interface ContentTypes {
}

export interface CountInfringements {
	potential_infringements?: number
	verified_infringements?: number
	takedown_pending?: number
	takedown_successful?: number
	non_infringements?: number
	total?: number
	unread?: number
}

export interface Credentials {
	username: string
	password: string
}

export interface DiskComponent {
	total: number
	used: number
	free: number
	percent: number
}

export interface HTTPValidationError {
	detail: ValidationError[]
}

export interface Infrastructure {
	createdAt: Date
	updatedAt: Date
	_id?: string
	vps: string
	ip: string
	cpu: number
	ram: MemoryComponent
	disk: DiskComponent
	gpu?: any[]
	components?: InfrastructureComponent[]
	last_checkin?: Date
}

export interface InfrastructureComponent {
	createdAt: Date
	updatedAt: Date
	_id?: string
	type: string
	name: string
	status: string
	metadata?: any
}

export interface Infringement {
	contentId: string
	personId: string
	source: string
	status?: InfringementStatus
	createdAt: Date
	updatedAt: Date
	_id?: string
	details?: any
	readAt: Date | null
	lastUpdateRead?: boolean
	owner: string
}

export interface InfringementPreferences {
	createdAt: Date
	updatedAt: Date
	receiveEmailOnDetection?: boolean
	automaticApproveInfringements?: boolean
	receiveEmailOnTakedown?: boolean
	sendTakedownRequests?: boolean
}

export interface InfringementRequest {
	contentId: string
	personId: string
	source: string
	status?: InfringementStatus
}

export interface InfringementStatus {
}

export interface Level {
}

export interface MemoryComponent {
	available: number
	total: number
	used: number
	free: number
	percent: number
}

export interface NotificationPreferences {
	receiveNewsletter?: boolean
	receivePromotions?: boolean
}

export interface OutsetaLoginResponse {
	access_token: string
	token_type: string
	expires_in: number
}

export interface PaginatedResults {
	pagination: any
	results: any[]
}

export interface PendingTasks {
	id: number
	name: string
	type: string
	lastRun: Date | null
	errors: number
}

export interface Person {
	username: string
	name: string
	email: string
	role: UserRoles
	createdAt: Date
	updatedAt: Date
	_id?: string
	accountId?: string
	accountStageLabel?: string
	automaticVerify?: boolean
	subscriptionId?: string
	infringementPreferences?: InfringementPreferences
	notificationPreferences?: NotificationPreferences
	allowedDomains?: string[]
	createdBy?: string
	owner: string | null
	seats?: number
	plan_type?: string
	profileImg?: string
	signature?: string
	country?: string
	company?: string
}

export interface PotentialVAResponse {
	potential_va: number
}

export interface Subscription {
	createdAt: Date
	updatedAt: Date
	_id?: string
	personId: string
	planId: string
	startDate?: Date
	endDate: Date | null
	status?: string
	scription_id?: string
}

export interface UpdateSubscriptionData {
	seats: number
	plan_type: string
}

export interface UserRoles {
}

export interface ValidationError {
	loc: string[] | number[]
	msg: string
	type: string
}

export interface FastapiCompatBodyUpdateInfringementPreferences1 {
	preferences: InfringementPreferences
}

export interface FastapiCompatBodyUpdateInfringementPreferences2 {
	preferences: InfringementPreferences
}

