import { useParams } from "react-router-dom"
import { useRegatta } from "../hooks/useRegatta"
import { useRegattaEditions } from "../hooks/useRegattaEditions"
import { EditionRegattaItem } from "../../editions/components/EditionRegattaItem"
import { ClipLoader } from "react-spinners"
import { CollapsibleSection } from "../../../shared/components/CollapsibleSection"
import { FeedbackButton } from "../../feedback/components/FeedbackButton"

export const RegattaDetailPage = () => {
    const { id } = useParams()

    const { regatta, loading, error } = useRegatta(id)
    const { editions, loading: loadingEditions } = useRegattaEditions(id)

    if (loading) 
        return (
            <div className="flex justify-center items-center p-10">
                <ClipLoader size={30} color={"#3b82f6"} />
            </div>
        )
    if (error) return <p className="p-4">{error}</p>

    if (!regatta) return <p className="p-4">No data</p>

    return (
        <div className="p-4 space-y-4">
            <div className="flex items-center">
                <h1 className="text-2xl font-bold">
                    {regatta.name}
                </h1>
                <div className="ml-auto">
                    <FeedbackButton
                        entityType="regatta"
                        entityId={Number(id)}
                    />
                </div>
            </div>

            <div className="space-y-1">
                {regatta.type && <p><strong>Type:</strong> {regatta.type}</p>}
                {regatta.club_name && <p><strong>Club:</strong> {regatta.club_name}</p>}
                {regatta.city && <p><strong>City:</strong> {regatta.city}</p>}
                {regatta.region && <p><strong>Region:</strong> {regatta.region}</p>}
                {regatta.country && <p><strong>Country:</strong> {regatta.country}</p>}

                <CollapsibleSection title="Editions" count={regatta.number_of_editions}>

                    {loadingEditions && <p>Loading editions...</p>}

                    {!loadingEditions && editions.length === 0 && (
                        <p>No editions found</p>
                    )}

                    <ul className="mt-2 space-y-2">
                        {editions.map((edition) => (
                            <EditionRegattaItem key={edition.id_edition} edition={edition}/>
                        ))}
                    </ul>
                </CollapsibleSection>
            </div>
        </div>
    )
}