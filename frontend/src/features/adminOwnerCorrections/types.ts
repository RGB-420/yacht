export type AdminOwnerCorrectionItem = {
    row_id: number
    raw_name?: string | null
    canonical_name?: string | null
    status?: string | null
    confidence?: string | null
    entity_type?: string | null
    notes?: string | null
}

export type PaginatedAdminOwnerCorrections = {
    data: AdminOwnerCorrectionItem[]
    total: number
    limit: number
    offset: number
    metrics: Record<string, number>
}

export type UpdateAdminOwnerCorrectionItem = {
    canonical_name?: string | null
    status?: string | null
    confidence?: string | null
    entity_type?: string | null
    notes?: string | null
}

export type AdminOwnerCorrectionOptions = {
    statuses: string[]
    entity_types: string[]
    suggestions: string[]
    sorts: string[]
}
