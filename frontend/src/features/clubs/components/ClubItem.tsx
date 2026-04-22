import { Link } from "react-router-dom"
import type { ClubsListItem} from "../types"
import { MapPinHouse } from "lucide-react"

interface Props {
    club: ClubsListItem
}

export const ClubItem = ({ club }: Props) => {

    const location = [club.city, club.country]
        .filter(Boolean)
        .join(", ")

    return (
        <li>
            <Link
                to={`/clubs/${club.id_club}`}
                className="block p-4 rounded-xl border border-border dark:border-borderDark
                           bg-surface dark:bg-surfaceDark text-text dark:text-textDark
                           hover:bg-primary dark:hover:bg-primaryDark transition-colors"
            >
                <p className="font-semibold text-lg">
                    {club.name}
                </p>

            {location && (
                <div className="flex items-center gap-2 text-sm">
                    <MapPinHouse size={12} />
                    <span>{location}</span>
                </div>
            )}
            </Link>
        </li>
    )
}