export interface EditionListItem {
    id_edition: number
    year: number
    status: "past" | "future"
}

export interface EditionDetail {
    id_edition: number
    year: number
    id_regatta: number
    regatta_name: string
    number_of_boats: number
    number_of_classes: number
    status: "past" | "future"
}

export interface EditionClasses {
    id_class: number
    name: string

    number_of_boats: number
}

export interface EditionLink {
    id_link: number
    url: string
    year: number
}