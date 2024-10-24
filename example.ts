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
  
  