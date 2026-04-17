import { useState } from "react"
import { useRegattas } from "../hooks/useRegattas"
import { RegattaItem } from "../components/RegattaItem"
import { PaginationControls } from "../../../shared/components/PaginationControls"

export const RegattasPage = () => {
    const [page, setPage] = useState(1)
    const [limit, setLimit] = useState(50)

    const { regattas, total, loading, error } = useRegattas(page, limit)

    if (loading) return <p className="p-4">Loading...</p>
    if (error) return <p className="p-4">{error}</p>

    return (
        <div className="p-4 space-y-4">
            <h1 className="text-2xl font-bold">Regattas</h1>

            <div className="grid gap-4">
                {regattas.map((r) => (
                    <RegattaItem key={r.id_regatta} regatta={r} />
                ))}
            </div>

            <PaginationControls
                page={page}
                total={total}
                limit={limit}
                onPageChange={setPage}
                onLimitChange={setLimit}
                pageSizeOptions={[10, 20, 50, 100]}
            />
        </div>
    )
}