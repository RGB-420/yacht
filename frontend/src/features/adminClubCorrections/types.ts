export type AdminClubCorrectionItem = {
    row_id: number
    club_raw_name?: string | null
    club_canonical_name?: string | null
    status?: string | null
    confidence?: string | null
    notes?: string | null
    regatta?: string | null
}

export type PaginatedAdminClubCorrections = {
    data: AdminClubCorrectionItem[]
    total: number
    limit: number
    offset: number
    metrics: Record<string, number>
}

export type UpdateAdminClubCorrectionItem = {
    club_canonical_name?: string | null
    status?: string | null
    confidence?: string | null
    notes?: string | null
}

export type AdminClubCorrectionOptions = {
    statuses: string[]
    suggestions: string[]
    sorts: string[]
}
