import { useEffect, useState } from "react"
import { getEditionById } from "../api/getEditionById"
import type { EditionDetail } from "../types"

export const useEdition = (id?: string) => {
    const [edition, setEdition] = useState<EditionDetail | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!id) return

        setLoading(true)

        getEditionById(id)
            .then(setEdition)
            .catch(() => setError("Error loading edition"))
            .finally(() => setLoading(false))
    }, [id])

    return { edition, loading, error}
}