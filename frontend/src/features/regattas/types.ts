export interface Regatta {
  id_regatta: number
  name: string
  type?: string
  club_name?: string | null
  city?: string | null
  region?: string | null
  country?: string | null
  number_of_editions?: number
}

export interface PaginatedRegattas {
  data: Regatta[]
  total: number
  limit: number
  offset: number
}