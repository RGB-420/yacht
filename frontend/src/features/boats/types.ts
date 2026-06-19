export interface BoatListItem {
    id_boat: number
    name: string
    boat_identifier?: string | null
    class_ids: number[]
    classes: string[]
}

export interface BoatDetail {
    id_boat: number
    name: string
    boat_identifier?: string | null

    classes_ids: number[]
    classes: string[]

    type_ids: number[]
    types: string[]

    owners: string[]
    clubs: string[]
}

export interface BoatEdition { 
    id_edition: number
    year: number
    id_regatta: number
    regatta_name: string
    status: "past" | "future"

    city?: string | null
    region?: string | null
    country?: string | null
}

export interface PaginatedBoats {
  data: BoatListItem[]
  total: number
  limit: number
  offset: number
}