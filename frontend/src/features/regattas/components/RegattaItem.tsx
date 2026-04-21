import { Link } from "react-router-dom"
import { Flag, MapPin } from "lucide-react"
import type { Regatta } from "../types"

export const RegattaItem = ({ regatta }: { regatta: Regatta }) => {
    
    const location = [regatta.city, regatta.country]
        .filter(Boolean)
        .join(", ")

    return (
        <Link to={`/regattas/${regatta.id_regatta}`}>
            <div className="p-4 border rounded-xl shadow-sm hover:shadow-md hover:bg-gray-50 transition">

                <h2 className="text-lg font-semibold">
                    {regatta.name}
                </h2>

                {regatta.type && (
                    <div className="flex items-center gap-2 mt-1 text-sm text-gray-500">
                        <Flag size={12} />
                        <span>{regatta.type}</span>
                    </div>
                )}

                {location && (
                    <div className="flex items-center gap-2 text-sm text-gray-500">
                        <MapPin size={12} />
                        <span>{location}</span>
                    </div>
                )}

            </div>
        </Link>
    )
}