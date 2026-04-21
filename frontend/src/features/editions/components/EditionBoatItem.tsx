import { Link } from "react-router-dom"
import type { BoatEdition } from "../../boats/types"
import { Calendar } from "lucide-react"

export const EditionBoatItem = ({ edition }: { edition: BoatEdition }) => {
    return (
        <li>
            <Link
                to={`/editions/${edition.id_edition}`}
                className="flex justify-between items-center p-4 rounded-xl border border-border dark:border-borderDark hover:bg-primary dark:hover:bg-primaryDark transition"
                >
                
                <div className="flex flex-col">
                    <p className="text-base font-semibold">
                        {edition.regatta_name}
                    </p>

                    {edition.year && (
                        <div className="flex items-center gap-2 mt-1 text-sm opacity-80">
                            <Calendar size={16} />
                            <span>{edition.year}</span>
                        </div>
                        )}
                </div>

                <span
                    className={`text-xs px-2 py-1 rounded-full font-medium ${
                        edition.status === "future"
                        ? "bg-green-300 text-green-900"
                        : "bg-gray-300 text-gray-900"
                    }`}
                >
                    {edition.status === "future" ? "Future" : "Past"}
                </span>
            </Link>
        </li>
    )
}