export interface ClassesListItem {
    id_class: number
    name: string
    
    number_of_boats: number
}

export interface Class {
    id_class: number
    name: string

    manufacturer: string | null
    category: string | null
    rating_rule: string | null

    start_year: number | null
    crew_min: number | null
    crew_max: number | null

    length_m: number | null
    
    number_of_boats: number
}

export interface BoatClass { 
    id_boat: number
    name: string
    boat_identifier: string | null

    owners: string[]
}