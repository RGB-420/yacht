export interface BoatDetail {
    id_boat: number
    name: string
    boat_identifier?: string | null

    class_ids: number[]
    classes: string[]

    type_ids: number[]
    types: string[]

    owners: string[]

    club_ids: number[]
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

export interface BoatPreview {
    id_boat: number
    name: string
    boat_identifier?: string | null
}

export interface BoatListItem extends BoatPreview {
    class_ids: number[]
    classes: string[]
}
