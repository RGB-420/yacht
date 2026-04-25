import { useEffect, useState } from "react"
import { getEditionLinks } from "../api/getEditionLinks"
import type { EditionLink } from "../types"

export const useEditionLinks = (id?: string) => {
    const [links, setLinks] = useState<EditionLink[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!id) return 

        setLoading(true)

        getEditionLinks(id)
            .then(setLinks)
            .catch(() => setError("Error loading links"))
            .finally(() => setLoading(false))
    }, [id])

    return { links, loading, error }
}