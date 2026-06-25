export type AdminRegattaQueueItem = {
    source_id?: string | null
    regatta_name?: string | null
    type?: string | null
    year?: number | null
    status?: string | null
    scraper_name?: string | null
    scrape_active?: number | null
    source_type?: string | null
    scrape_status?: string | null
    specified_class?: string | null
    start_date?: string | null
    end_date?: string | null
    notes?: string | null
    city?: string | null
    region?: string | null
    country?: string | null
    link?: string | null
}

export type PaginatedAdminRegattas = {
    data: AdminRegattaQueueItem[]
    total: number
    limit: number
    offset: number
}

export type UpdateAdminRegattaQueueItem = {
    link?: string | null
    scraper_name?: string | null
    source_type?: string | null
    scrape_active?: number | null
    scrape_status?: string | null
    specified_class?: string | null
    notes?: string | null
}

export type CreateAdminRegattaQueueItem = {
    regatta_name: string
    year: number
    type?: string | null
    status?: string | null
    scraper_name?: string | null
    scrape_active?: number | null
    source_type?: string | null
    scrape_status?: string | null
    specified_class?: string | null
    start_date?: string | null
    end_date?: string | null
    notes?: string | null
    city?: string | null
    region?: string | null
    country?: string | null
    link?: string | null
}

export type AdminRegattaOptions = {
    scrapers: string[]
    source_types: string[]
    scrape_statuses: string[]
}
