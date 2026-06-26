import { Link } from "react-router-dom"
import { useState } from "react"
import { ClipLoader } from "react-spinners"
import { PaginationControls } from "../../../shared/components/PaginationControls"
import { AdminClassTypeCorrectionCard } from "../components/AdminClassTypeCorrectionCard"
import { useAdminClassTypeCorrections } from "../hooks/useAdminClassTypeCorrections"

export const AdminClassTypeCorrectionsPage = () => {
    const [page, setPage] = useState(1)
    const [limit, setLimit] = useState(25)
    const [status, setStatus] = useState("unresolved")
    const [shape, setShape] = useState("all")
    const [sortBy, setSortBy] = useState("raw_class")
    const [sortDir, setSortDir] = useState("asc")
    const [query, setQuery] = useState("")
    const {
        corrections,
        options,
        metrics,
        total,
        loading,
        savingId,
        error,
        saveCorrection
    } = useAdminClassTypeCorrections(page, limit, status, shape, sortBy, sortDir, query)

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
                    <h1 className="text-2xl font-bold">Class/Type Corrections</h1>
                    <p className="text-sm opacity-70">
                        {total} class/type mapping rows
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

            <div
                className="
                    p-4 rounded-xl
                    border border-border dark:border-borderDark
                    bg-background dark:bg-backgroundDark
                    grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3
                "
            >
                <label className="space-y-1 text-sm">
                    <span className="font-medium">Status</span>
                    <select
                        value={status}
                        onChange={(e) => {
                            setStatus(e.target.value)
                            setPage(1)
                        }}
                        className="
                            w-full p-2 rounded-lg
                            border border-border dark:border-borderDark
                            bg-background dark:bg-backgroundDark
                        "
                    >
                        <option value="all">all</option>
                        {options.statuses.map((option) => (
                            <option key={option} value={option}>
                                {option}
                            </option>
                        ))}
                    </select>
                </label>

                <label className="space-y-1 text-sm">
                    <span className="font-medium">Raw fields</span>
                    <select
                        value={shape}
                        onChange={(e) => {
                            setShape(e.target.value)
                            setPage(1)
                        }}
                        className="
                            w-full p-2 rounded-lg
                            border border-border dark:border-borderDark
                            bg-background dark:bg-backgroundDark
                        "
                    >
                        <option value="all">all</option>
                        <option value="missing_any_raw">missing class or type</option>
                        <option value="missing_raw_class">missing raw class</option>
                        <option value="missing_raw_type">missing raw type</option>
                        <option value="has_both_raw">has class and type</option>
                    </select>
                </label>

                <label className="space-y-1 text-sm">
                    <span className="font-medium">Sort by</span>
                    <select
                        value={sortBy}
                        onChange={(e) => {
                            setSortBy(e.target.value)
                            setPage(1)
                        }}
                        className="
                            w-full p-2 rounded-lg
                            border border-border dark:border-borderDark
                            bg-background dark:bg-backgroundDark
                        "
                    >
                        <option value="raw_class">raw class</option>
                        <option value="raw_type">raw type</option>
                        <option value="canonical_class">canonical class</option>
                        <option value="canonical_type">canonical type</option>
                        <option value="confidence">confidence</option>
                        <option value="status">status</option>
                    </select>
                </label>

                <label className="space-y-1 text-sm">
                    <span className="font-medium">Direction</span>
                    <select
                        value={sortDir}
                        onChange={(e) => {
                            setSortDir(e.target.value)
                            setPage(1)
                        }}
                        className="
                            w-full p-2 rounded-lg
                            border border-border dark:border-borderDark
                            bg-background dark:bg-backgroundDark
                        "
                    >
                        <option value="asc">ascending</option>
                        <option value="desc">descending</option>
                    </select>
                </label>

                <label className="space-y-1 text-sm">
                    <span className="font-medium">Search</span>
                    <input
                        value={query}
                        onChange={(e) => {
                            setQuery(e.target.value)
                            setPage(1)
                        }}
                        placeholder="Raw class, raw type or canonical value"
                        className="
                            w-full p-2 rounded-lg
                            border border-border dark:border-borderDark
                            bg-background dark:bg-backgroundDark
                        "
                    />
                </label>
            </div>

            <details
                className="
                    p-4 rounded-xl
                    border border-border dark:border-borderDark
                    bg-background dark:bg-backgroundDark
                "
            >
                <summary className="cursor-pointer font-semibold">
                    Mapping quality metrics
                </summary>

                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3 mt-4">
                    {[
                        ["total", "Total"],
                        ["pending", "Pending"],
                        ["resolved", "Resolved"],
                        ["unresolved", "Unresolved"],
                        ["ignored", "Ignored"],
                        ["missing_any_raw", "Missing raw"],
                        ["has_both_raw", "Has raw class/type"],
                        ["with_canonical_class", "With canonical class"],
                        ["with_canonical_type", "With canonical type"],
                        ["with_both_canonical", "With both canonical"],
                        ["missing_any_canonical", "Missing canonical"],
                        ["numeric_confidence", "Numeric confidence"],
                        ["non_numeric_confidence", "Manual confidence"]
                    ].map(([key, label]) => (
                        <div
                            key={key}
                            className="
                                p-3 rounded-lg
                                border border-border dark:border-borderDark
                            "
                        >
                            <p className="text-xl font-bold">{metrics[key] ?? 0}</p>
                            <p className="text-xs opacity-70">{label}</p>
                        </div>
                    ))}
                </div>
            </details>

            {corrections.length === 0 && (
                <p>No class/type corrections found</p>
            )}

            <div className="space-y-2">
                {corrections.map((correction) => (
                    <AdminClassTypeCorrectionCard
                        key={correction.row_id}
                        correction={correction}
                        options={options}
                        saving={savingId === correction.row_id}
                        onSave={saveCorrection}
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
