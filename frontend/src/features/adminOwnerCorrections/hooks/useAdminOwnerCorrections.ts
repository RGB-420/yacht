import { useEffect, useState } from "react"
import {
    getOwnerCorrectionOptions,
    getOwnerCorrections,
    updateOwnerCorrection
} from "../api/adminOwnerCorrectionsApi"
import type {
    AdminOwnerCorrectionItem,
    AdminOwnerCorrectionOptions,
    UpdateAdminOwnerCorrectionItem
} from "../types"

export const useAdminOwnerCorrections = (
    page: number,
    limit: number,
    status: string,
    entityType: string,
    suggestion: string,
    sortBy: string,
    sortDir: string,
    query: string
) => {
    const [corrections, setCorrections] = useState<AdminOwnerCorrectionItem[]>([])
    const [options, setOptions] = useState<AdminOwnerCorrectionOptions | null>(null)
    const [metrics, setMetrics] = useState<Record<string, number>>({})
    const [total, setTotal] = useState(0)
    const [loading, setLoading] = useState(true)
    const [savingId, setSavingId] = useState<number | null>(null)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true)
                setError(null)

                const offset = (page - 1) * limit
                const [correctionsRes, optionsRes] = await Promise.all([
                    getOwnerCorrections(limit, offset, status, entityType, suggestion, sortBy, sortDir, query),
                    getOwnerCorrectionOptions()
                ])

                setCorrections(correctionsRes.data)
                setTotal(correctionsRes.total)
                setMetrics(correctionsRes.metrics)
                setOptions(optionsRes)
            } catch (err) {
                setError("Error loading owner corrections")
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [page, limit, status, entityType, suggestion, sortBy, sortDir, query])

    const saveCorrection = async (
        rowId: number,
        data: UpdateAdminOwnerCorrectionItem
    ) => {
        const previous = corrections

        try {
            setSavingId(rowId)
            setError(null)

            const updated = await updateOwnerCorrection(rowId, data)

            setCorrections((current) =>
                current.map((correction) =>
                    correction.row_id === rowId ? updated : correction
                )
            )
        } catch (err) {
            setCorrections(previous)
            setError("Error saving owner correction")
        } finally {
            setSavingId(null)
        }
    }

    return {
        corrections,
        options,
        metrics,
        total,
        loading,
        savingId,
        error,
        saveCorrection
    }
}
