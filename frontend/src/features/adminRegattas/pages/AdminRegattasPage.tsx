import { Link } from "react-router-dom"
import { useState } from "react"
import { ClipLoader } from "react-spinners"
import { PaginationControls } from "../../../shared/components/PaginationControls"
import { AddRegattaForm } from "../components/AddRegattaForm"
import { AdminRegattaCard } from "../components/AdminRegattaCard"
import { useAdminRegattas } from "../hooks/useAdminRegattas"

export const AdminRegattasPage = () => {
    const [page, setPage] = useState(1)
    const [limit, setLimit] = useState(25)
    const {
        regattas,
        options,
        total,
        loading,
        savingId,
        adding,
        error,
        saveRegatta,
        addRegatta
    } = useAdminRegattas(page, limit)

    if (loading)
        return (
            <div className="flex justify-center items-center p-10">
                <ClipLoader size={30} color={"#3b82f6"} />
            </div>
        )
    if (error) return <p className="p-4">{error}</p>
    if (!options) return <p className="p-4">No options</p>

    return (
        <div className="p-4 space-y-4">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-2xl font-bold">Regattas Admin</h1>
                    <p className="text-sm opacity-70">
                        {total} unscraped regattas
                    </p>
                </div>

                <Link
                    to="/admin"
                    className="
                        text-sm px-3 py-1 rounded-xl
                        border border-border dark:border-borderDark
                        hover:bg-primary hover:text-white
                        transition-colors
                    "
                >
                    Admin
                </Link>
            </div>

            <AddRegattaForm
                options={options}
                adding={adding}
                onAdd={addRegatta}
            />

            {regattas.length === 0 && (
                <p>No unscraped regattas found</p>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                {regattas.map((regatta) => (
                    <AdminRegattaCard
                        key={regatta.source_id}
                        regatta={regatta}
                        options={options}
                        saving={savingId === regatta.source_id}
                        onSave={saveRegatta}
                    />
                ))}
            </div>

            <PaginationControls
                page={page}
                total={total}
                limit={limit}
                onPageChange={setPage}
                onLimitChange={setLimit}
                pageSizeOptions={[10, 25, 50, 100]}
            />
        </div>
    )
}
