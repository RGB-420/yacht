export type CoverageMetric = {
    key: string
    label: string
    total: number
    covered: number
    missing: number
    coverage_pct: number
}

export type BoatQualityMetrics = {
    total_boats: number
    coverage: CoverageMetric[]
    boats_with_multiple_types: number
}

export type BoatQualityIssueSample = {
    id_boat: number
    name: string
    boat_identifier?: string | null
    types?: string[] | null
    classes?: string[] | null
    owners?: string[] | null
    clubs?: string[] | null
}

export type BoatQualityIssueGroup = {
    key: string
    label: string
    total: number
    samples: BoatQualityIssueSample[]
}

export type BoatQualityIssueDetail = BoatQualityIssueGroup & {
    limit: number
    offset: number
}

export type BoatQualityIssues = {
    limit: number
    issues: BoatQualityIssueGroup[]
}
