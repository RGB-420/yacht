export interface SearchItem {
    id: number
    name: string
    type: string
}

export interface SearchResult {
    boats: SearchItem[]
    regattas: SearchItem[]
    classes: SearchItem[]
    clubs: SearchItem[]
}