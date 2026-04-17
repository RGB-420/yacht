import { Link } from "react-router-dom"
import type { BoatListItem } from "../types"


export const BoatItem = ({ boat }: { boat: BoatListItem }) => {
    return (
    <li> 
        <Link
        to={`/boats/${boat.id_boat}`}
        className="flex justify-between items-center p-3 border rounded-lg hover:bg-gray-50 transition"
        >
        <span className="font-medium">{boat.name}</span>

        {boat.boat_identifier && (
            <span className="text-sm text-gray-500">
            {boat.boat_identifier}
            </span>
        )}
        </Link>
    </li>)
}