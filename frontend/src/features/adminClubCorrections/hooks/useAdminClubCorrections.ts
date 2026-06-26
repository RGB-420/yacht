import { useEffect, useState } from "react"
import {
    getClubCorrectionOptions,
    getClubCorrections,
    updateClubCorrection
} from "../api/adminClubCorrectionsApi"
import type {
    AdminClubCorrectionItem,
    AdminClubCorrectionOptions,
    UpdateAdminClubCorrectionItem
} from "../types"

export const useAdminClubCorrections = (
    page: number,
    limit: number,
    status: string,
    suggestion: string,
    sortBy: string,
    sortDir: string,
    query: string
) => {
    const [corrections, setCorrections] = useState<AdminClubCorrectionItem[]>([])
    const [options, setOptions] = useState<AdminClubCorrectionOptions | null>(null)
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
                    getClubCorrections(limit, offset, status, suggestion, sortBy, sortDir, query),
                    getClubCorrectionOptions()
                ])

                setCorrections(correctionsRes.data)
                setTotal(correctionsRes.total)
                setMetrics(correctionsRes.metrics)
                setOptions(optionsRes)
            } catch (err) {
                setError("Error loading club corrections")
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [page, limit, status, suggestion, sortBy, sortDir, query])

    const saveCorrection = async (
        rowId: number,
        data: UpdateAdminClubCorrectionItem
    ) => {
        const previous = corrections

        try {
            setSavingId(rowId)
            setError(null)

            const updated = await updateClubCorrection(rowId, data)

            setCorrections((current) =>
                current.map((correction) =>
                    correction.row_id === rowId ? updated : correction
                )
            )
        } catch (err) {
            setCorrections(previous)
            setError("Error saving club correction")
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
