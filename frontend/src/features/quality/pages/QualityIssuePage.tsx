import { Link, useParams } from "react-router-dom"
import { useState } from "react"
import { ClipLoader } from "react-spinners"
import { PaginationControls } from "../../../shared/components/PaginationControls"
import { QualityIssueSampleCard } from "../components/QualityIssueCard"
import { useBoatQualityIssue } from "../hooks/useBoatQualityIssue"

export const QualityIssuePage = () => {
    const { issueKey } = useParams()
    const [page, setPage] = useState(1)
    const [limit, setLimit] = useState(50)
    const { issue, loading, error } = useBoatQualityIssue(issueKey, page, limit)

    if (loading)
        return (
            <div className="flex justify-center items-center p-10">
                <ClipLoader size={30} color={"#3b82f6"} />
            </div>
        )
    if (error) return <p className="p-4">{error}</p>
    if (!issue) return <p className="p-4">No data</p>

    return (
        <div className="p-4 space-y-4">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-2xl font-bold">
                        {issue.label}
                    </h1>
                    <p className="text-sm opacity-70">
                        Showing {issue.samples.length} of {issue.total}
                    </p>
                </div>

                <Link
                    to="/admin/quality"
                    className="
                        text-sm px-3 py-1 rounded-xl
                        border border-border dark:border-borderDark
                        hover:bg-primary hover:text-white
                        transition-colors
                    "
                >
                    Quality
                </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {issue.samples.map((sample) => (
                    <QualityIssueSampleCard
                        key={sample.id_boat}
                        sample={sample}
                    />
                ))}
            </div>

            <PaginationControls
                page={page}
                total={issue.total}
                limit={limit}
                onPageChange={setPage}
                onLimitChange={setLimit}
                pageSizeOptions={[25, 50, 100, 200]}
            />
        </div>
    )
}
