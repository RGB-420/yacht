import { Link } from "react-router-dom"
import { Layers } from "lucide-react"
import type { ClassesListItem } from "../types"

interface Props {
    cls: ClassesListItem
}

export const ClassItem = ({ cls }: Props) => {
    return (
        <li>
            <Link
                to={`/classes/${cls.id_class}`}
                className="block p-4 rounded-xl border border-border dark:border-borderDark
                           bg-surface dark:bg-surfaceDark text-text dark:text-textDark
                           hover:bg-primary dark:hover:bg-primaryDark transition-colors"
            >
                <p className="font-semibold text-lg">
                    {cls.name}
                </p>

                <div className="flex items-center gap-2 mt-1 text-sm opacity-80">
                    <Layers size={16} />
                    <span>{cls.number_of_boats} boats</span>
                </div>
            </Link>
        </li>
    )
}