import { Link } from "react-router-dom"
import type { EditionListItem } from "../types"

export const EditionRegattaItem = ({ edition }: { edition: EditionListItem }) => {
    return (
        <li>
            <Link
                to={`/editions/${edition.id_edition}`}
                className="flex justify-between items-center p-3 border rounded-lg hover:bg-gray-50 transition"
            >
                <span className="font-medium text-lg">
                    {edition.year}
                </span>

                <span
                    className={`text-xs px-2 py-1 rounded-full font-medium ${
                        edition.status === "future"
                        ? "bg-green-100 text-green-700"
                        : "bg-gray-200 text-gray-700"
                    }`}
                >
                    {edition.status === "future" ? "Future" : "Past"}
                </span>
            </Link>
        </li>
    )
}
