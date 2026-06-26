import { useEffect, useState } from "react"
import {
    getClassTypeCorrectionOptions,
    getClassTypeCorrections,
    updateClassTypeCorrection
} from "../api/adminClassTypeCorrectionsApi"
import type {
    AdminClassTypeCorrectionItem,
    AdminClassTypeCorrectionOptions,
    UpdateAdminClassTypeCorrectionItem
} from "../types"

export const useAdminClassTypeCorrections = (
    page: number,
    limit: number,
    status: string,
    shape: string,
    sortBy: string,
    sortDir: string,
    query: string
) => {
    const [corrections, setCorrections] = useState<AdminClassTypeCorrectionItem[]>([])
    const [options, setOptions] = useState<AdminClassTypeCorrectionOptions | null>(null)
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
                    getClassTypeCorrections(limit, offset, status, shape, sortBy, sortDir, query),
                    getClassTypeCorrectionOptions()
                ])

                setCorrections(correctionsRes.data)
                setTotal(correctionsRes.total)
                setMetrics(correctionsRes.metrics)
                setOptions(optionsRes)
            } catch (err) {
                setError("Error loading class/type corrections")
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [page, limit, status, shape, sortBy, sortDir, query])

    const saveCorrection = async (
        rowId: number,
        data: UpdateAdminClassTypeCorrectionItem
    ) => {
        const previous = corrections

        try {
            setSavingId(rowId)
            setError(null)

            const updated = await updateClassTypeCorrection(rowId, data)

            setCorrections((current) =>
                current.map((correction) =>
                    correction.row_id === rowId ? updated : correction
                )
            )
        } catch (err) {
            setCorrections(previous)
            setError("Error saving class/type correction")
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
