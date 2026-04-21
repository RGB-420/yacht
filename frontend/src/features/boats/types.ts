export interface BoatListItem {
    id_boat: number
    name: string
    boat_identifier?: string | null
    id_class?: number | null
    class_name?: string | null
}

export interface BoatDetail {
    id_boat: number
    name: string
    boat_identifier?: string | null

    id_class?: number | null
    class_name?: string | null

    id_type?: number | null
    type_name?: string | null

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