import { useEffect, useState } from "react"
import { getBoatById } from "../api/getBoatById"
import type { BoatDetail } from "../types"

export const useBoat = (id?: string) => {
    const [boat, setBoat] = useState<BoatDetail | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!id) return

        setLoading(true)

        getBoatById(id)
            .then(setBoat)
            .catch(() => setError("Error loading boat"))
            .finally(() => setLoading(false))
    }, [id])

    return { boat, loading, error }
}