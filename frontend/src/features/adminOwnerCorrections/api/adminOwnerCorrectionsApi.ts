import { apiFetch } from "../../../shared/api/client"
import type {
    AdminOwnerCorrectionItem,
    AdminOwnerCorrectionOptions,
    PaginatedAdminOwnerCorrections,
    UpdateAdminOwnerCorrectionItem
} from "../types"

const getAdminKey = () => localStorage.getItem("admin_code")

const adminHeaders = () => ({
    "x-admin-key": getAdminKey() || ""
})

export const getOwnerCorrections = async (
    limit = 50,
    offset = 0,
    status = "pending",
    entityType = "all",
    suggestion = "all",
    sortBy = "raw_name",
    sortDir = "asc",
    query = ""
): Promise<PaginatedAdminOwnerCorrections> => {
    const params = new URLSearchParams({
        limit: String(limit),
        offset: String(offset),
        status,
        entity_type: entityType,
        suggestion,
        sort_by: sortBy,
        sort_dir: sortDir
    })

    if (query) {
        params.set("q", query)
    }

    return apiFetch(`/admin/corrections/owners?${params.toString()}`, {
        headers: adminHeaders()
    })
}

export const updateOwnerCorrection = async (
    rowId: number,
    data: UpdateAdminOwnerCorrectionItem
): Promise<AdminOwnerCorrectionItem> => {
    return apiFetch(`/admin/corrections/owners/${rowId}`, {
        method: "PATCH",
        headers: adminHeaders(),
        body: JSON.stringify(data)
    })
}

export const getOwnerCorrectionOptions = async (): Promise<AdminOwnerCorrectionOptions> => {
    return apiFetch("/admin/corrections/owners/options", {
        headers: adminHeaders()
    })
}
