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
            className="w-full p-3 border rounded-lg"
        />
    )
}