import { useEffect, useState } from "react"
import {
    addRegattaToQueue,
    getAdminRegattaOptions,
    getUnscrapedRegattas,
    updateUnscrapedRegatta
} from "../api/adminRegattasApi"
import type {
    AdminRegattaOptions,
    AdminRegattaQueueItem,
    CreateAdminRegattaQueueItem,
    UpdateAdminRegattaQueueItem
} from "../types"

export const useAdminRegattas = (page: number, limit: number) => {
    const [regattas, setRegattas] = useState<AdminRegattaQueueItem[]>([])
    const [options, setOptions] = useState<AdminRegattaOptions | null>(null)
    const [total, setTotal] = useState(0)
    const [loading, setLoading] = useState(true)
    const [savingId, setSavingId] = useState<string | null>(null)
    const [adding, setAdding] = useState(false)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true)
                setError(null)

                const offset = (page - 1) * limit
                const [regattasRes, optionsRes] = await Promise.all([
                    getUnscrapedRegattas(limit, offset),
                    getAdminRegattaOptions()
                ])

                setRegattas(regattasRes.data)
                setTotal(regattasRes.total)
                setOptions(optionsRes)
            } catch (err) {
                setError("Error loading admin regattas")
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [page, limit])

    const saveRegatta = async (
        sourceId: string,
        data: UpdateAdminRegattaQueueItem
    ) => {
        const previous = regattas

        try {
            setSavingId(sourceId)
            setError(null)

            const updated = await updateUnscrapedRegatta(sourceId, data)

            setRegattas((current) =>
                current.map((regatta) =>
                    regatta.source_id === sourceId ? updated : regatta
                )
            )
        } catch (err) {
            setRegattas(previous)
            setError("Error saving regatta")
        } finally {
            setSavingId(null)
        }
    }

    const addRegatta = async (data: CreateAdminRegattaQueueItem) => {
        try {
            setAdding(true)
            setError(null)

            await addRegattaToQueue(data)
        } catch (err) {
            setError("Error adding regatta to queue")
            throw err
        } finally {
            setAdding(false)
        }
    }

    return {
        regattas,
        options,
        total,
        loading,
        savingId,
        adding,
        error,
        saveRegatta,
        addRegatta
    }
}
