import { Link } from "react-router-dom"
import type { Regatta } from "../types"

export const RegattaItem = ({ regatta }: { regatta: Regatta}) => {
    return (
        <Link to={`/regattas/${regatta.id_regatta}`}>
            <div className="p-4 border rounded-xl shadow hover:shadow-lg transition">
                <h2 className="text-lg font-bold">{regatta.name}</h2>
            </div>
        </Link>
    )
}