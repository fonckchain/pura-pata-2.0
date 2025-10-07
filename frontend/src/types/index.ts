export interface User {
  id: string
  email: string
  name: string
  phone: string
  location?: string
  created_at: string
}

export interface Dog {
  id: string
  name: string
  age_years: number
  age_months: number
  breed: string
  size: 'pequeño' | 'mediano' | 'grande'
  gender: 'macho' | 'hembra'
  color: string
  description?: string

  vaccinated: boolean
  sterilized: boolean
  dewormed: boolean
  special_needs?: string

  latitude: number
  longitude: number
  address?: string
  province?: string

  contact_phone: string
  contact_email?: string

  photos: string[]
  certificate?: string

  status: 'disponible' | 'reservado' | 'adoptado'

  publisher_id: string
  publisher?: User

  created_at: string
  updated_at: string
  adopted_at?: string
}

export interface DogStatusHistory {
  id: string
  dog_id: string
  old_status?: string
  new_status: string
  changed_at: string
}

export interface DogFormData {
  name: string
  age_years: number
  age_months: number
  breed: string
  size: 'pequeño' | 'mediano' | 'grande'
  gender: 'macho' | 'hembra'
  color: string
  description?: string
  vaccinated: boolean
  sterilized: boolean
  dewormed: boolean
  special_needs?: string
  latitude: number
  longitude: number
  address?: string
  province?: string
  contact_phone: string
  contact_email?: string
  photos: File[]
  certificate?: File
}

export interface SearchFilters {
  size?: 'pequeño' | 'mediano' | 'grande'
  gender?: 'macho' | 'hembra'
  age_min?: number
  age_max?: number
  province?: string
  latitude?: number
  longitude?: number
  radius_km?: number
}
