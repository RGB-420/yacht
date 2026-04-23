import { useState, useRef, useEffect } from "react"
import { Link } from "react-router-dom"
import { useSearch } from "../../search/hooks/useSearch"
import { SearchInput } from "../components/SearchInput"
import { SearchDropdown } from "../components/SearchDropdown"
import { ThemeToggle } from "../../../shared/components/ThemeToggle"
import { Sailboat, Flag, Boxes, University } from "lucide-react"

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
            
            <div className="absolute top-4 left-4">
                <ThemeToggle />
            </div>

            <h1 className="text-3xl sm:text-5xl font-bold text-center">
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

                {loading}

                {results && (
                    <SearchDropdown
                        results={results}
                        query={query}
                        isOpen={isOpen}
                        setIsOpen={setIsOpen}
                    />
                )}
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <Link
                    to="/regattas"
                    className="flex flex-col items-center justify-center p-4 w-full border-2 border-border dark:border-borderDark rounded-xl hover:bg-primary dark:hover:bg-primaryDark transition-colors"
                    >
                    <Flag size={28}/>
                    <span className="mt-2 text-sm font-medium">
                        Regattas
                    </span>
                </Link>

                <Link
                    to="/boats"
                    className="flex flex-col items-center justify-center p-4 w-full border-2 border-border dark:border-borderDark rounded-xl hover:bg-primary dark:hover:bg-primaryDark transition-colors"
                    >
                    <Sailboat size={28}/>
                    <span className="mt-2 text-sm font-medium">
                        Boats
                    </span>
                </Link>

                <Link
                    to="/classes"
                    className="flex flex-col items-center justify-center p-4 w-full border-2 border-border dark:border-borderDark rounded-xl hover:bg-primary dark:hover:bg-primaryDark transition-colors"
                    >
                    <Boxes size={28}/>
                    <span className="mt-2 text-sm font-medium">
                        Classes
                    </span>
                </Link>

                <Link
                    to="/clubs"
                    className="flex flex-col items-center justify-center p-4 w-full border-2 border-border dark:border-borderDark rounded-xl hover:bg-primary dark:hover:bg-primaryDark transition-colors"
                    >
                    <University size={28}/>
                    <span className="mt-2 text-sm font-medium">
                        Clubs
                    </span>
                </Link>
            </div>
        </div>
    )
}