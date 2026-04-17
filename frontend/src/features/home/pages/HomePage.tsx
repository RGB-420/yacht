import { useState, useRef, useEffect } from "react"
import { Link } from "react-router-dom"
import { useSearch } from "../../search/hooks/useSearch"
import { SearchInput } from "../components/SearchInput"
import { SearchDropdown } from "../components/SearchDropdown"
import { Sailboat, Flag } from "lucide-react"

export const HomePage = () => {
    const [query, setQuery] = useState("")
    const [isOpen, setIsOpen] = useState(false)
    const { results, loading } = useSearch(query)
    const ref = useRef<HTMLDivElement>(null)

    useEffect(() => {
        const handleClickOutside = (e: MouseEvent) => {
            if (ref.current && !ref.current.contains(e.target as Node)) {
                setIsOpen(false)
            }
        }

        document.addEventListener("mousedown", handleClickOutside)

        return () => {
            document.removeEventListener("mousedown", handleClickOutside)
        }
    }, [])

    return (
        <div ref={ref} className="p-6 max-w-2xl mx-auto space-y-8 relative">
        
            <h1 className="text-3xl font-bold text-center">
                Regatta Explorer
            </h1>

            <SearchInput
                query={query}
                setQuery={setQuery}
                setIsOpen={setIsOpen}
            />

            {loading && <p>Searching...</p>}

            {results && (
                <SearchDropdown
                    results={results}
                    query={query}
                    isOpen={isOpen}
                    setIsOpen={setIsOpen}
                />
            )}

            <div className="flex justify-center gap-6 mt-6">
                <Link
                    to="/regattas"
                    className="flex flex-col items-center justify-center p-4 w-24 border rounded-xl hover:bg-gray-100 transition"
                    >
                    <Flag size={20}/>
                </Link>

                <Link
                    to="/boats"
                    className="flex flex-col items-center justify-center p-4 w-24 border rounded-xl hover:bg-gray-100 transition"
                    >
                    <Sailboat size={20}/>
                </Link>
            </div>
        </div>
    )
}