import { Link, useNavigate } from "react-router-dom"
import { ClipLoader } from "react-spinners"
import { QualityIssueCard } from "../components/QualityIssueCard"
import { QualityMetricCard } from "../components/QualityMetricCard"
import { useBoatQuality } from "../hooks/useBoatQuality"

export const QualityDashboardPage = () => {
    const { metrics, issues, loading, error } = useBoatQuality()
    const navigate = useNavigate()

    const handleLogout = () => {
        localStorage.removeItem("isAdmin")
        localStorage.removeItem("admin_code")

        navigate("/")
    }

    if (loading) 
        return (
            <div className="flex justify-center items-center p-10">
                <ClipLoader size={30} color={"#3b82f6"} />
            </div>
        )
    if (error) return <p className="p-4">{error}</p>
    if (!metrics || !issues) return <p className="p-4">No data</p>

    return (
        <div className="p-4 space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-2xl font-bold">Data Quality</h1>
                    <p className="text-sm opacity-70">
                        Boats coverage and issue samples
                    </p>
                </div>

                <div className="flex items-center gap-2">
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

                    <button 
                        onClick={handleLogout}
                        className="
                            text-sm px-3 py-1 rounded-xl
                            border border-border dark:border-borderDark
                            hover:bg-red-500 hover:text-white
                            transition-colors    
                        "
                    >
                        Logout
                    </button>
                </div>
            </div>

            <section className="space-y-3">
                <div>
                    <h2 className="text-lg font-semibold">Boats</h2>
                    <p className="text-sm opacity-70">
                        {metrics.total_boats} total boats
                    </p>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {metrics.coverage.map((metric) => (
                        <QualityMetricCard
                            key={metric.key}
                            metric={metric}
                        />
                    ))}
                </div>

                <div
                    className="
                        p-4 rounded-xl
                        border border-border dark:border-borderDark
                        bg-background dark:bg-backgroundDark
                    "
                >
                    <p className="font-semibold">Multiple types</p>
                    <p className="text-sm opacity-70">
                        {metrics.boats_with_multiple_types} boats have more than one type
                    </p>
                </div>
            </section>

            <section className="space-y-3">
                <div>
                    <h2 className="text-lg font-semibold">Issue Samples</h2>
                    <p className="text-sm opacity-70">
                        Showing {issues.limit} examples per issue
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {issues.issues.map((issue) => (
                        <Link
                            key={issue.key}
                            to={`/admin/quality/boats/issues/${issue.key}`}
                            className="block hover:shadow-md transition-shadow rounded-xl"
                        >
                            <QualityIssueCard
                                issue={issue}
                            />
                        </Link>
                    ))}
                </div>
            </section>
        </div>
    )
}
