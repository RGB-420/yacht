import { Link } from "react-router-dom"
import type { EditionListItem } from "../types"
import { Calendar } from "lucide-react"

export const EditionRegattaItem = ({ edition }: { edition: EditionListItem }) => {
    return (
        <li>
            <Link
                to={`/editions/${edition.id_edition}`}
                className="flex justify-between items-center p-3 border rounded-lg hover:bg-primary dark:hover:bg-primaryDark transition"
            >
                <span className="flex font-medium items-center text-lg gap-2">
                    <Calendar size={16} /> {edition.year}
                </span>

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
