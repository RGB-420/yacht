import { useState } from "react"
import type {
    AdminOwnerCorrectionItem,
    AdminOwnerCorrectionOptions,
    UpdateAdminOwnerCorrectionItem
} from "../types"

type Props = {
    correction: AdminOwnerCorrectionItem
    options: AdminOwnerCorrectionOptions
    saving: boolean
    onSave: (rowId: number, data: UpdateAdminOwnerCorrectionItem) => void
}

const toInputValue = (value?: string | null) => {
    if (value === null || value === undefined) return ""

    return value
}

export const AdminOwnerCorrectionCard = ({
    correction,
    options,
    saving,
    onSave
}: Props) => {
    const [form, setForm] = useState<UpdateAdminOwnerCorrectionItem>({
        canonical_name: correction.canonical_name || "",
        status: correction.status || "pending",
        confidence: correction.confidence || "",
        entity_type: correction.entity_type || "UNKNOWN",
        notes: correction.notes || ""
    })

    const updateField = (
        key: keyof UpdateAdminOwnerCorrectionItem,
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
                grid grid-cols-1 xl:grid-cols-[1.4fr_1.4fr_130px_110px_110px_1fr_auto]
                gap-2 items-start
            "
        >
            <div className="min-w-0">
                <p className="text-xs font-medium opacity-60">Raw owner</p>
                <p className="text-sm font-semibold break-words">
                    {correction.raw_name || "-"}
                </p>
            </div>

            <label className="space-y-1 text-xs">
                <span className="font-medium opacity-60">Canonical</span>
                <input
                    value={toInputValue(form.canonical_name)}
                    onChange={(e) => updateField("canonical_name", e.target.value)}
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
                <span className="font-medium opacity-60">Entity</span>
                <select
                    value={toInputValue(form.entity_type)}
                    onChange={(e) => updateField("entity_type", e.target.value)}
                    className="
                        w-full p-1.5 rounded-md text-sm
                        border border-border dark:border-borderDark
                        bg-background dark:bg-backgroundDark
                    "
                >
                    {options.entity_types.map((entityType) => (
                        <option key={entityType} value={entityType}>
                            {entityType}
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

            <div className="flex xl:justify-end pt-5">
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
