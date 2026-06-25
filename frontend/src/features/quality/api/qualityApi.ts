import { apiFetch } from "../../../shared/api/client"
import type { BoatQualityIssueDetail, BoatQualityIssues, BoatQualityMetrics } from "../types"

const getAdminKey = () => localStorage.getItem("admin_code")

const adminHeaders = () => ({
    "x-admin-key": getAdminKey() || ""
})

export const getBoatQualityMetrics = async (): Promise<BoatQualityMetrics> => {
    return apiFetch("/admin/quality/boats", {
        headers: adminHeaders()
    })
}

export const getBoatQualityIssues = async (limit = 10): Promise<BoatQualityIssues> => {
    return apiFetch(`/admin/quality/boats/issues?limit=${limit}`, {
        headers: adminHeaders()
    })
}

export const getBoatQualityIssue = async (
    issueKey: string,
    limit = 100,
    offset = 0
): Promise<BoatQualityIssueDetail> => {
    return apiFetch(`/admin/quality/boats/issues/${issueKey}?limit=${limit}&offset=${offset}`, {
        headers: adminHeaders()
    })
}
