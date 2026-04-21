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
        <div className="min-h-[80vh] flex flex-col items-center justify-center space-y-8">
        
            <h1 className="text-5xl font-bold text-center">
                Regatta Explorer
            </h1>

            <p className="text-gray-500 text-center max-w-md">
            Explore boats, regattas and editions in one place
            </p>

            <div ref={ref} className="relative w-full max-w-xl">
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
            </div>
            <div className="flex justify-center gap-10 mt-4">
                <Link
                    to="/regattas"
                    className="flex flex-col items-center justify-center p-4 w-24 border rounded-xl hover:bg-gray-100 transition"
                    >
                    <Flag size={28}/>
                    <span className="mt-2 text-sm font-medium">
                        Regattas
                    </span>
                </Link>

                <Link
                    to="/boats"
                    className="flex flex-col items-center justify-center p-4 w-24 border rounded-xl hover:bg-gray-100 transition"
                    >
                    <Sailboat size={28}/>
                    <span className="mt-2 text-sm font-medium">
                        Boats
                    </span>
                </Link>
            </div>
        </div>
    )
}