import { useParams } from "react-router-dom"
import { Link } from "react-router-dom"
import { useEdition } from "../hooks/useEdition"
import { useEditionBoats } from "../hooks/useEditionBoats"
import { BoatItem } from "../../boats/components/BoatItem"
import { Calendar, Flag } from "lucide-react"
import { ClipLoader } from "react-spinners"

export const EditionDetailPage = () => {
    const { id } = useParams()

    const { edition, loading, error } = useEdition(id)
    const { boats, loading: loadingBoats } = useEditionBoats(id)

    if (loading) 
        return (
            <div className="flex justify-center items-center p-10">
                <ClipLoader size={30} color={"#3b82f6"} />
            </div>
        )
    if (error) return <p className="p-4">{error}</p>
    if (!edition) return <p className="p-4">No data</p>

    return (
        <div className="p-4 space-y-4">
            <div className="flex items-center">
                <h1 className="text-2xl font-bold">
                    {edition.regatta_name}
                </h1>

                <div
                    className="ml-auto"
                    >
                    <Link
                        to={`/regattas/${edition.id_regatta}`}
                        className="inline-flex items-center gap-2 px-3 py-2 border-2 border-border dark:border-borderDark rounded-xl text-text dark:text-textDark hover:bg-primary dark:hover:bg-primaryDark hover:text-white transition-colors"
                        >
                        <Flag size={20}/>
                        <span className="text-sm font-medium">
                            Go to Regatta
                        </span>
                    </Link>
                </div>
            </div>
            <div className="flex items-center gap-2 mt-1 text-sm">
                <Calendar size={20} />
                <span className="text-xl font-semibold"> {edition.year}</span>
            </div>

            <div className="space-y-1">
                <p><strong>Boats:</strong> {edition.number_of_boats}</p>
                <p><strong>Classes:</strong> {edition.number_of_classes}</p>
            </div>
            <div className="mt-6">
                <h2 className="text-xl font-semibold">Boats</h2>

                {loadingBoats && <p>Loading boats...</p>}

                {!loadingBoats && boats.length === 0 && (
                    <p>No boats found</p>
                )}

                <ul className="mt-2 space-y-2">
                    {boats.map((boat) => (
                        <BoatItem key={boat.id_boat} boat={boat} />
                    ))}
                </ul>
            </div>
        </div>
    )
}
