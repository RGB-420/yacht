import { Link } from "react-router-dom"
import { Sailboat } from "lucide-react"
import type { BoatListItem } from "../types"

interface Props {
  boat: BoatListItem
}

export const BoatItem = ({ boat }: Props) => {
  return (
    <li>
      <Link
        to={`/boats/${boat.id_boat}`}
        className="block p-4 border rounded-xl hover:shadow-md hover:bg-gray-50 transition"
      >
        
        {/* 🔹 Nombre */}
        <p className="font-semibold text-lg">
          {boat.name}
        </p>

        {/* 🔹 ID debajo */}
        {boat.boat_identifier && (
          <div className="flex items-center gap-2 mt-1 text-sm text-gray-500">
            <Sailboat size={14} />
            <span>{boat.boat_identifier}</span>
          </div>
        )}

      </Link>
    </li>
  )
}