import { apiFetch } from "../../../shared/api/client"
import type {
    AdminClassTypeCorrectionItem,
    AdminClassTypeCorrectionOptions,
    PaginatedAdminClassTypeCorrections,
    UpdateAdminClassTypeCorrectionItem
} from "../types"

const getAdminKey = () => localStorage.getItem("admin_code")

const adminHeaders = () => ({
    "x-admin-key": getAdminKey() || ""
})

export const getClassTypeCorrections = async (
    limit = 50,
    offset = 0,
    status = "unresolved",
    shape = "all",
    sortBy = "raw_class",
    sortDir = "asc",
    query = ""
): Promise<PaginatedAdminClassTypeCorrections> => {
    const params = new URLSearchParams({
        limit: String(limit),
        offset: String(offset),
        status,
        shape,
        sort_by: sortBy,
        sort_dir: sortDir
    })

    if (query) {
        params.set("q", query)
    }

    return apiFetch(`/admin/corrections/class-types?${params.toString()}`, {
        headers: adminHeaders()
    })
}

export const updateClassTypeCorrection = async (
    rowId: number,
    data: UpdateAdminClassTypeCorrectionItem
): Promise<AdminClassTypeCorrectionItem> => {
    return apiFetch(`/admin/corrections/class-types/${rowId}`, {
        method: "PATCH",
        headers: adminHeaders(),
        body: JSON.stringify(data)
    })
}

export const getClassTypeCorrectionOptions = async (): Promise<AdminClassTypeCorrectionOptions> => {
    return apiFetch("/admin/corrections/class-types/options", {
        headers: adminHeaders()
    })
}
