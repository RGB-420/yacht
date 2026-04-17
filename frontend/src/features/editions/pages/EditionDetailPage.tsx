import { useParams } from "react-router-dom"
import { Link } from "react-router-dom"
import { useEdition } from "../hooks/useEdition"
import { useEditionBoats } from "../hooks/useEditionBoats"
import { BoatItem } from "../../boats/components/BoatItem"

export const EditionDetailPage = () => {
    const { id } = useParams()

    const { edition, loading, error } = useEdition(id)
    const { boats, loading: loadingBoats } = useEditionBoats(id)

    if (loading) return <p className="p-4">Loading...</p>
    if (error) return <p className="p-4">{error}</p>
    if (!edition) return <p className="p-4">No data</p>

    return (
        <div className="p-4 space-y-4">
            <h1 className="text-2xl font-bold">
                <Link
                    to={`/regattas/${edition.id_regatta}`}
                    className="hover:underline"
                >
                    {edition.regatta_name}
                </Link>{" "}    
                {edition.year}
            </h1>

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
