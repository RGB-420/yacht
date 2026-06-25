import { apiFetch } from "../../../shared/api/client"
import type {
    AdminRegattaOptions,
    AdminRegattaQueueItem,
    CreateAdminRegattaQueueItem,
    PaginatedAdminRegattas,
    UpdateAdminRegattaQueueItem
} from "../types"

const getAdminKey = () => localStorage.getItem("admin_code")

const adminHeaders = () => ({
    "x-admin-key": getAdminKey() || ""
})

export const getUnscrapedRegattas = async (
    limit = 50,
    offset = 0
): Promise<PaginatedAdminRegattas> => {
    return apiFetch(`/admin/regattas/unscraped?limit=${limit}&offset=${offset}`, {
        headers: adminHeaders()
    })
}

export const updateUnscrapedRegatta = async (
    sourceId: string,
    data: UpdateAdminRegattaQueueItem
): Promise<AdminRegattaQueueItem> => {
    return apiFetch(`/admin/regattas/unscraped/${encodeURIComponent(sourceId)}`, {
        method: "PATCH",
        headers: adminHeaders(),
        body: JSON.stringify(data)
    })
}

export const addRegattaToQueue = async (
    data: CreateAdminRegattaQueueItem
): Promise<AdminRegattaQueueItem> => {
    return apiFetch("/admin/regattas/queue", {
        method: "POST",
        headers: adminHeaders(),
        body: JSON.stringify(data)
    })
}

export const getAdminRegattaOptions = async (): Promise<AdminRegattaOptions> => {
    return apiFetch("/admin/regattas/options", {
        headers: adminHeaders()
    })
}
