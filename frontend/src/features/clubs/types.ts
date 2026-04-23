export interface ClubsListItem {
    id_club: number
    name: string

    short_name: string | null

    city: string | null
    region: string | null
    country: string | null
}

export interface Club {
    id_club: number
    name: string

    short_name: string | null
    estimated_numbers: number | null

    city: string | null
    region: string | null
    country: string | null

    number_of_boats: number
    number_of_regattas: number
}

export interface ClubBoats {
    id_boat: number
    name: string
    boat_identifier: string
}

export interface ClubRegattas {
    id_regatta: number
    name: string

    city: string | null
    region: string | null
    country: string | null
}