import { useEffect, useState } from "react"
import { getBoats } from "../api/getBoats"
import type { BoatListItem } from "../types"

export const useBoats = (page: number, limit:number) => {
    const [boats, setBoats] = useState<BoatListItem[]>([])
    const [total, setTotal] = useState(0)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        setLoading(true)

        getBoats(page, limit)
            .then((res) => {
                setBoats(res.data)
                setTotal(res.total)
            })
            .catch(() => setError("Error loading boats"))
            .finally(() => setLoading(false))
    }, [page, limit])

    return { boats, total, loading, error}
}