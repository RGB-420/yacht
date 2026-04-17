import { useEffect, useState } from "react"
import { getSearch } from "../api/getSearch"
import type { SearchResult } from "../types"

export const useSearch = (query: string) => {
    const [results, setResults] = useState<SearchResult | null>(null)
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        if (query.length < 2) return

        setLoading(true)

        const timeout = setTimeout(() => {
            getSearch(query)
                .then(setResults)
                .finally(() => setLoading(false))
        }, 300)

        return () => clearTimeout(timeout)
    }, [query])

    return { results, loading }
}