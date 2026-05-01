import { useState } from "react"
import { Settings } from "lucide-react"
import { AdminModal } from "./AdminModal"
import { useNavigate } from "react-router-dom"

const ADMIN_CODE = import.meta.env.VITE_ADMIN_CODE

export const AdminAccess = () => {
    const [open, setOpen] = useState(false)
    const [code, setCode] = useState("")
    const [error, setError] = useState(false)

    const navigate = useNavigate()

    const handleLogin = () => {
        if (code === ADMIN_CODE) {
            localStorage.setItem("isAdmin", "true")
            localStorage.setItem("admin_code", code)
            setOpen(false)
            setCode("")
            setError(false)

            navigate("/admin/feedback")
        } else {
            setError(true)
            setCode("")
        }
    }

    return (
        <>
            <button
                onClick={() => setOpen(true)}
                className="
                    fixed bottom-4 right-4
                    opacity-20 hover:opacity-0
                    text-xs
                    bg-background dark:bg-backgroundDark
                    border border:border dark:border-borderDark
                    px-2 py-1 rounded-lg
                    shadow    
                "
            >
                <Settings size={24} />
            </button>

            <AdminModal
                open={open}
                code={code}
                error={error}
                onClose={() => setOpen(false)}
                onChange={(value) => {
                    setCode(value)
                    setError(false)
                }}
                onSubmit={handleLogin}
            />
        </>
    )
}