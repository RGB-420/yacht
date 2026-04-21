import { useLocation } from "react-router-dom"
import { Navbar } from "../shared/components/Navbar"
import { AppRoutes } from "./routes"

export const Layout = () => {
    const location = useLocation()

    const hideNavbar = location.pathname === "/"

    return (
         <div className="min-h-screen bg-background dark:bg-backgroundDark text-text dark:text-textDark transition-colors">

            {!hideNavbar && <Navbar />}

            <div className="max-w-4xl mx-auto p-6">
                <AppRoutes />
            </div>

        </div>
    )
}