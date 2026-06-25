import type { BoatQualityIssueGroup, BoatQualityIssueSample } from "../types"
import { Sailboat } from "lucide-react"

type Props = {
    issue: BoatQualityIssueGroup
}

const formatList = (values?: string[] | null) => {
    if (!values || values.length === 0) return "None"

    return values.join(", ")
}

export const QualityIssueSampleCard = ({ sample }: { sample: BoatQualityIssueSample }) => {
    return (
        <li
            className="
                p-3 rounded-lg
                border border-border dark:border-borderDark
                space-y-2
            "
        >
            <p className="font-semibold text-lg">
                {sample.name}
            </p>
            
            <div className="flex justify-between gap-3">
                <div>
                    <div className="flex items-center gap-2 mt-1 text-sm">
                        <Sailboat size={16} />
                        <span>{sample.boat_identifier}</span>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                <p>
                    <span className="font-medium">Types:</span> {formatList(sample.types)}
                </p>
                <p>
                    <span className="font-medium">Classes:</span> {formatList(sample.classes)}
                </p>
                <p>
                    <span className="font-medium">Owners:</span> {formatList(sample.owners)}
                </p>
                <p>
                    <span className="font-medium">Clubs:</span> {formatList(sample.clubs)}
                </p>
            </div>
        </li>
    )
}

export const QualityIssueCard = ({ issue }: Props) => {
    return (
        <div
            className="
                p-4 rounded-xl
                border border-border dark:border-borderDark
                bg-background dark:bg-backgroundDark
                space-y-3
            "
        >
            <div className="flex justify-between items-center gap-3">
                <h2 className="font-semibold">
                    {issue.label}
                </h2>

                <span className="text-sm opacity-70">
                    {issue.total}
                </span>
            </div>

            {issue.samples.length === 0 && (
                <p className="text-sm opacity-70">
                    No examples found
                </p>
            )}

            <ul className="list-none space-y-2">
                {issue.samples.map((sample) => (
                    <QualityIssueSampleCard
                        key={sample.id_boat}
                        sample={sample}
                    />
                ))}
            </ul>
        </div>
    )
}
