import { Link } from "react-router-dom"
import type { BoatEdition } from "../../boats/types"

export const EditionBoatItem = ({ edition }: { edition: BoatEdition }) => {
    return (
        <li>
            <Link
            to={`/editions/${edition.id_edition}`}
            className="flex justify-between items-center p-3 border rounded-lg hover:bg-gray-50 transition"
            >
            <span className="font-medium">
                {edition.year} {edition.regatta_name}
            </span>
            </Link>
        </li>
    )
}