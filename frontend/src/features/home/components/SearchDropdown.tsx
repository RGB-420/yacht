import { Link } from "react-router-dom"
import type { SearchResult } from "../../search/types"


interface Props {
    results: SearchResult
    query: string
    isOpen: boolean
    setIsOpen: (value: boolean) => void
}

export const SearchDropdown = ({ results, query, isOpen, setIsOpen }: Props) => {
    if (!results || query.length < 2 || !isOpen) return null

    return (
        <div className="absolute w-full bg-background dark:bg-backgroundDark border border-border dark:border-borderDark rounded-lg shadow-lg mt-1 z-10">

            {results.boats.length > 0 && (
                <div>
                    <p className="px-3 py-2 text-s text-gray-500">Boats</p>
                    {results.boats.map((item) => (
                        <Link
                            key={item.id}
                            to={`/boats/${item.id}`}
                            onClick={() => setIsOpen(false)}
                            className="block px-3 py-2 hover:bg-primary dark:hover:bg-primaryDark"
                        >
                            {item.name}
                        </Link>
                    ))}
                </div>
            )}

            {results.regattas.length > 0 && (
                <div>
                    <p className="px-3 py-2 text-s text-gray-500">Regattas</p>
                    {results.regattas.map((item) => (
                        <Link
                            key={item.id}
                            to={`/regattas/${item.id}`}
                            onClick={() => setIsOpen(false)}
                            className="block px-3 py-2 hover:bg-primary dark:hover:bg-primaryDark"
                        >
                            {item.name}
                        </Link>
                    ))}
                </div>
            )}
        </div>
    )
}