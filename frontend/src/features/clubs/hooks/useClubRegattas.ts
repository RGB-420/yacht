import { useEffect, useState } from "react"
import { getClubRegattas } from "../api/getClubRegattas"
import type { ClubRegattas } from "../types"

export const useClubRegattas = (id?: string) => {
    const [regattas, setRegattas] = useState<ClubRegattas[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    
    useEffect(() => {
        if (!id) return

        setLoading(true)

        getClubRegattas(id)
            .then(setRegattas)
            .catch(() => setError("Error loading regattas"))
            .finally(() => setLoading(false))
    }, [id])

    return { regattas, loading, error }
}