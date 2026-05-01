import { useState } from "react"
import { useFeedbackList } from "../hooks/useFeedbackList"
import { FeedbackCard } from "../components/FeedbackCard"
import { ClipLoader } from "react-spinners"
import { FeedbackTabs } from "../components/FeedbackTabs"
import { useNavigate } from "react-router-dom"

export const FeedbackPage = () => {
    const { data, loading, error, changeStatus } = useFeedbackList()
    const [activeTab, setActiveTab] = useState<
        "all" | "pending" | "reviewed" | "fixed" | "ignored" | "suggestions"
        >("pending")

    const filteredData = data.filter((item) => {
        if (activeTab === "all") return true
        if (activeTab === "suggestions")
            return item.type === "regatta_suggestion"
        
        return item.status === activeTab
    })

    const counts = {
        all: data.length,
        pending: data.filter(f => f.status === "pending").length,
        reviewed: data.filter(f => f.status === "reviewed").length,
        fixed: data.filter(f => f.status === "fixed").length,
        ignored: data.filter(f => f.status === "ignored").length,
        suggestions: data.filter(f => f.type === "regatta_suggestion").length
    }

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

    return (
        <div className="p-4 space-y-4">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold">Feedback</h1>

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
            
            <FeedbackTabs
                active={activeTab}
                onChange={setActiveTab}
                counts={counts}
            />

            {data.length === 0 && (
                <p>No feedback in this tab</p>
            )}

            {filteredData.map((item) => (
                <FeedbackCard
                    key={item.id_feedback}
                    item={item}
                    onChangeStatus={changeStatus}
                />
            ))}
        </div>
    )
}