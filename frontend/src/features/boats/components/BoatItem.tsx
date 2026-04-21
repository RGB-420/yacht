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
        className="block p-4 border rounded-xl hover:shadow-md hover:bg-primary dark:hover:bg-primaryDark transition"
      >
        
        <p className="font-semibold text-lg">
          {boat.name}
        </p>

        {boat.boat_identifier && (
          <div className="flex items-center gap-2 mt-1 text-sm">
            <Sailboat size={16} />
            <span>{boat.boat_identifier}</span>
          </div>
        )}

      </Link>
    </li>
  )
}