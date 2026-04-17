import { useEffect, useState } from "react"
import { getRegattas } from "../api/getRegattas"
import type { Regatta } from "../types"

export const useRegattas = (page: number, limit:number) => {
    const [regattas, setRegattas] = useState<Regatta[]>([])
    const [total, setTotal] = useState(0)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        getRegattas(page, limit)
            .then((res) => {
                setRegattas(res.data)
                setTotal(res.total)
            })
            .catch(() => setError("Error loading regattas"))
            .finally(() => setLoading(false))
    }, [page, limit])

    return { regattas, total, loading, error}
}

