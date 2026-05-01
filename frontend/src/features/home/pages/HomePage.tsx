import { useState, useRef, useEffect } from "react"
import { Link } from "react-router-dom"
import { useSearch } from "../../search/hooks/useSearch"
import { SearchInput } from "../components/SearchInput"
import { SearchDropdown } from "../components/SearchDropdown"
import { ThemeToggle } from "../../../shared/components/ThemeToggle"
import { AdminAccess } from "../../admin/components/AdminAccess"
import { home_links } from "../../../shared/config/homeNavigation"

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

            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4 w-full max-w-3xl">
                {home_links.map((item) => {
                    const Icon = item.icon

                    return (
                        <Link
                            key={item.to}
                            to={item.to}
                            className="
                                flex flex-col items-center justify-center
                                p-4
                                border border-border dark:border-borderDark
                                rounded-xl
                                hover:bg-primary dark:hover:bg-primaryDark
                                hover:text-white
                                transition-all duration-200
                                group
                            "
                        >
                            <Icon size={30} className="group-hover:scale-110 transition-transform" />

                            <span className="mt-2 text-sm font-medium">
                                {item.label}
                            </span>
                        </Link>
                    )
                })}
            </div>

            <div className="absolute bottom-4 right-4 opacity-20 hover:opacity-100 transition">
                <AdminAccess />
            </div>
        </div>
    )
}