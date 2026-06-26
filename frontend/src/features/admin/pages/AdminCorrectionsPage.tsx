import { Layers, Sailboat, UserRound } from "lucide-react"
import { Link } from "react-router-dom"

export const AdminCorrectionsPage = () => {
    return (
        <div className="p-4 space-y-4">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-2xl font-bold">Corrections</h1>
                    <p className="text-sm opacity-70">
                        Review and maintain mapping rules used by the pipelines
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

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Link
                    to="/admin/corrections/clubs"
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
                        <Sailboat size={26} />
                        <div>
                            <p className="font-semibold">Club Corrections</p>
                            <p className="text-sm opacity-70">
                                Review and resolve club mapping rules
                            </p>
                        </div>
                    </div>
                </Link>

                <Link
                    to="/admin/corrections/class-types"
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
                        <Layers size={26} />
                        <div>
                            <p className="font-semibold">Class/Type Corrections</p>
                            <p className="text-sm opacity-70">
                                Review and resolve class and boat type mapping rules
                            </p>
                        </div>
                    </div>
                </Link>

                <Link
                    to="/admin/corrections/owners"
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
                        <UserRound size={26} />
                        <div>
                            <p className="font-semibold">Owner Corrections</p>
                            <p className="text-sm opacity-70">
                                Review and resolve owner prenormalization rules
                            </p>
                        </div>
                    </div>
                </Link>
            </div>
        </div>
    )
}
