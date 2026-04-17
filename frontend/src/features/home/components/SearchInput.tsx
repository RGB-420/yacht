interface Props {
    query: string
    setQuery: (value: string) => void
    setIsOpen: (value: boolean) => void
}

export const SearchInput = ({ query, setQuery, setIsOpen }: Props) => {
    return (
        <input
            type="text"
            placeholder="Search boats, regattas..."
            value={query}
            onChange={(e) => {
                setQuery(e.target.value) 
                setIsOpen(true)
            }}
            className="w-full max-w-xl p-4 text-lg border rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
    )
}