import { Link } from "react-router-dom"
import { useState } from "react"
import { ClipLoader } from "react-spinners"
import { PaginationControls } from "../../../shared/components/PaginationControls"
import { AdminOwnerCorrectionCard } from "../components/AdminOwnerCorrectionCard"
import { useAdminOwnerCorrections } from "../hooks/useAdminOwnerCorrections"

export const AdminOwnerCorrectionsPage = () => {
    const [page, setPage] = useState(1)
    const [limit, setLimit] = useState(25)
    const [status, setStatus] = useState("pending")
    const [entityType, setEntityType] = useState("all")
    const [suggestion, setSuggestion] = useState("all")
    const [sortBy, setSortBy] = useState("raw_name")
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
    } = useAdminOwnerCorrections(page, limit, status, entityType, suggestion, sortBy, sortDir, query)

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
                    <h1 className="text-2xl font-bold">Owner Corrections</h1>
                    <p className="text-sm opacity-70">
                        {total} owner mapping rows
                    </p>
                </div>

                <Link
                    to="/admin/corrections"
                    className="
                        text-sm px-3 py-1 rounded-xl
                        border border-border dark:border-borderDark
                        hover:bg-primary hover:text-white
                        transition-colors
                    "
                >
                    Corrections
                </Link>
            </div>

            <div
                className="
                    p-4 rounded-xl
                    border border-border dark:border-borderDark
                    bg-background dark:bg-backgroundDark
                    grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-3
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
                    <span className="font-medium">Entity</span>
                    <select
                        value={entityType}
                        onChange={(e) => {
                            setEntityType(e.target.value)
                            setPage(1)
                        }}
                        className="
                            w-full p-2 rounded-lg
                            border border-border dark:border-borderDark
                            bg-background dark:bg-backgroundDark
                        "
                    >
                        <option value="all">all</option>
                        {options.entity_types.map((option) => (
                            <option key={option} value={option}>
                                {option}
                            </option>
                        ))}
                    </select>
                </label>

                <label className="space-y-1 text-sm">
                    <span className="font-medium">Suggestion</span>
                    <select
                        value={suggestion}
                        onChange={(e) => {
                            setSuggestion(e.target.value)
                            setPage(1)
                        }}
                        className="
                            w-full p-2 rounded-lg
                            border border-border dark:border-borderDark
                            bg-background dark:bg-backgroundDark
                        "
                    >
                        <option value="all">all</option>
                        <option value="with_suggestion">with canonical suggestion</option>
                        <option value="without_suggestion">without canonical suggestion</option>
                        <option value="high_numeric_confidence">numeric confidence &gt;= 90</option>
                        <option value="low_numeric_confidence">numeric confidence &lt; 90</option>
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
                        <option value="raw_name">raw name</option>
                        <option value="canonical_name">canonical name</option>
                        <option value="confidence">confidence</option>
                        <option value="entity_type">entity type</option>
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
                        placeholder="Raw owner, canonical or notes"
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
                        ["with_suggestion", "With suggestion"],
                        ["without_suggestion", "Without suggestion"],
                        ["high_numeric_confidence", "Confidence >= 90"],
                        ["low_numeric_confidence", "Confidence < 90"],
                        ["entity_type_person", "Person"],
                        ["entity_type_company", "Company"],
                        ["entity_type_club", "Club"],
                        ["entity_type_unknown", "Unknown"],
                        ["entity_type_invalid", "Invalid"]
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
                <p>No owner corrections found</p>
            )}

            <div className="space-y-2">
                {corrections.map((correction) => (
                    <AdminOwnerCorrectionCard
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
