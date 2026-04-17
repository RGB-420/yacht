import { useEffect, useState } from "react"
import { getRegattaById } from "../api/getRegattaById"
import type { Regatta } from "../types"

export const useRegatta = (id?: string) => {
    const [regatta, setRegatta] = useState<Regatta | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!id) return

        setLoading(true)

        getRegattaById(id)
            .then(setRegatta)
            .catch(() => setError("Error loading regatta"))
            .finally(() => setLoading(false))
    }, [id])

    return { regatta, loading, error}
}
