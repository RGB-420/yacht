import { apiFetch } from "../../../shared/api/client"
import type {
    AdminClubCorrectionItem,
    AdminClubCorrectionOptions,
    PaginatedAdminClubCorrections,
    UpdateAdminClubCorrectionItem
} from "../types"

const getAdminKey = () => localStorage.getItem("admin_code")

const adminHeaders = () => ({
    "x-admin-key": getAdminKey() || ""
})

export const getClubCorrections = async (
    limit = 50,
    offset = 0,
    status = "pending",
    suggestion = "all",
    sortBy = "club_raw_name",
    sortDir = "asc",
    query = ""
): Promise<PaginatedAdminClubCorrections> => {
    const params = new URLSearchParams({
        limit: String(limit),
        offset: String(offset),
        status,
        suggestion,
        sort_by: sortBy,
        sort_dir: sortDir
    })

    if (query) {
        params.set("q", query)
    }

    return apiFetch(`/admin/corrections/clubs?${params.toString()}`, {
        headers: adminHeaders()
    })
}

export const updateClubCorrection = async (
    rowId: number,
    data: UpdateAdminClubCorrectionItem
): Promise<AdminClubCorrectionItem> => {
    return apiFetch(`/admin/corrections/clubs/${rowId}`, {
        method: "PATCH",
        headers: adminHeaders(),
        body: JSON.stringify(data)
    })
}

export const getClubCorrectionOptions = async (): Promise<AdminClubCorrectionOptions> => {
    return apiFetch("/admin/corrections/clubs/options", {
        headers: adminHeaders()
    })
}
