export type AdminClassTypeCorrectionItem = {
    row_id: number
    raw_class?: string | null
    raw_type?: string | null
    canonical_class?: string | null
    canonical_type?: string | null
    status?: string | null
    confidence?: string | null
    notes?: string | null
}

export type PaginatedAdminClassTypeCorrections = {
    data: AdminClassTypeCorrectionItem[]
    total: number
    limit: number
    offset: number
    metrics: Record<string, number>
}

export type UpdateAdminClassTypeCorrectionItem = {
    canonical_class?: string | null
    canonical_type?: string | null
    status?: string | null
    confidence?: string | null
    notes?: string | null
}

export type AdminClassTypeCorrectionOptions = {
    statuses: string[]
    shapes: string[]
    sorts: string[]
}
