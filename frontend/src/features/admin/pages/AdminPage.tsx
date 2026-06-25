import { BarChart3, MessageSquare } from "lucide-react"
import { Link, useNavigate } from "react-router-dom"

export const AdminPage = () => {
    const navigate = useNavigate()

    const handleLogout = () => {
        localStorage.removeItem("isAdmin")
        localStorage.removeItem("admin_code")

        navigate("/")
    }

    return (
        <div className="p-4 space-y-4">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold">Admin</h1>

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

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Link
                    to="/admin/quality"
                    className="
                        p-4 rounded-xl
                        border border-border dark:border-borderDark
                        bg-background dark:bg-backgroundDark
                        hover:bg-primary dark:hover:bg-primaryDark
                        hover:text-white
                        transition-all duration-200
                    "
                >
                    <div className="flex items-center gap-3">
                        <BarChart3 size={26} />
                        <div>
                            <p className="font-semibold">Quality</p>
                            <p className="text-sm opacity-70">
                                Review coverage and data quality metrics
                            </p>
                        </div>
                    </div>
                </Link>

                <Link
                    to="/admin/feedback"
                    className="
                        p-4 rounded-xl
                        border border-border dark:border-borderDark
                        bg-background dark:bg-backgroundDark
                        hover:bg-primary dark:hover:bg-primaryDark
                        hover:text-white
                        transition-all duration-200
                    "
                >
                    <div className="flex items-center gap-3">
                        <MessageSquare size={26} />
                        <div>
                            <p className="font-semibold">Feedback</p>
                            <p className="text-sm opacity-70">
                                Review user feedback and suggestions
                            </p>
                        </div>
                    </div>
                </Link>
            </div>
        </div>
    )
}
