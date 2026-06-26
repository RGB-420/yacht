import { useState } from "react"
import type {
    AdminClubCorrectionItem,
    AdminClubCorrectionOptions,
    UpdateAdminClubCorrectionItem
} from "../types"

type Props = {
    correction: AdminClubCorrectionItem
    options: AdminClubCorrectionOptions
    saving: boolean
    onSave: (rowId: number, data: UpdateAdminClubCorrectionItem) => void
}

const toInputValue = (value?: string | null) => {
    if (value === null || value === undefined) return ""

    return value
}

export const AdminClubCorrectionCard = ({
    correction,
    options,
    saving,
    onSave
}: Props) => {
    const [form, setForm] = useState<UpdateAdminClubCorrectionItem>({
        club_canonical_name: correction.club_canonical_name || "",
        status: correction.status || "pending",
        confidence: correction.confidence || "",
        notes: correction.notes || ""
    })

    const updateField = (
        key: keyof UpdateAdminClubCorrectionItem,
        value: string
    ) => {
        setForm((current) => ({
            ...current,
            [key]: value
        }))
    }

    return (
        <div
            className="
                p-3 rounded-lg
                border border-border dark:border-borderDark
                bg-background dark:bg-backgroundDark
                grid grid-cols-1 lg:grid-cols-[1.3fr_1.3fr_140px_100px_1fr_auto]
                gap-2 items-start
            "
        >
            <div className="min-w-0">
                <p className="text-xs font-medium opacity-60">Raw</p>
                <p className="text-sm font-semibold break-words">
                    {correction.club_raw_name}
                </p>
                <p className="text-xs opacity-60 break-words">
                    {correction.regatta || "No regatta source"}
                </p>
            </div>

            <label className="space-y-1 text-xs">
                <span className="font-medium opacity-60">Canonical</span>
                <input
                    value={toInputValue(form.club_canonical_name)}
                    onChange={(e) => updateField("club_canonical_name", e.target.value)}
                    className="
                        w-full p-1.5 rounded-md text-sm
                        border border-border dark:border-borderDark
                        bg-background dark:bg-backgroundDark
                    "
                />
            </label>

            <label className="space-y-1 text-xs">
                <span className="font-medium opacity-60">Status</span>
                <select
                    value={toInputValue(form.status)}
                    onChange={(e) => updateField("status", e.target.value)}
                    className="
                        w-full p-1.5 rounded-md text-sm
                        border border-border dark:border-borderDark
                        bg-background dark:bg-backgroundDark
                    "
                >
                    {options.statuses.map((status) => (
                        <option key={status} value={status}>
                            {status}
                        </option>
                    ))}
                </select>
            </label>

            <label className="space-y-1 text-xs">
                <span className="font-medium opacity-60">Confidence</span>
                <input
                    value={toInputValue(form.confidence)}
                    onChange={(e) => updateField("confidence", e.target.value)}
                    className="
                        w-full p-1.5 rounded-md text-sm
                        border border-border dark:border-borderDark
                        bg-background dark:bg-backgroundDark
                    "
                />
            </label>

            <label className="space-y-1 text-xs">
                <span className="font-medium opacity-60">Notes</span>
                <input
                    value={toInputValue(form.notes)}
                    onChange={(e) => updateField("notes", e.target.value)}
                    className="
                        w-full p-1.5 rounded-md text-sm
                        border border-border dark:border-borderDark
                        bg-background dark:bg-backgroundDark
                    "
                />
            </label>

            <div className="flex lg:justify-end pt-5">
                <button
                    disabled={saving}
                    onClick={() => onSave(correction.row_id, form)}
                    className="
                        px-3 py-1.5 rounded-md text-sm
                        bg-primary dark:bg-primaryDark
                        text-white
                        disabled:opacity-50
                    "
                >
                    {saving ? "Saving..." : "Save"}
                </button>
            </div>
        </div>
    )
}
