import { useState } from "react"
import type {
    AdminClassTypeCorrectionItem,
    AdminClassTypeCorrectionOptions,
    UpdateAdminClassTypeCorrectionItem
} from "../types"

type Props = {
    correction: AdminClassTypeCorrectionItem
    options: AdminClassTypeCorrectionOptions
    saving: boolean
    onSave: (rowId: number, data: UpdateAdminClassTypeCorrectionItem) => void
}

const toInputValue = (value?: string | null) => {
    if (value === null || value === undefined) return ""

    return value
}

export const AdminClassTypeCorrectionCard = ({
    correction,
    options,
    saving,
    onSave
}: Props) => {
    const [form, setForm] = useState<UpdateAdminClassTypeCorrectionItem>({
        canonical_class: correction.canonical_class || "",
        canonical_type: correction.canonical_type || "",
        status: correction.status || "pending",
        confidence: correction.confidence || "",
        notes: correction.notes || ""
    })

    const updateField = (
        key: keyof UpdateAdminClassTypeCorrectionItem,
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
                grid grid-cols-1 xl:grid-cols-[1.2fr_1.2fr_1.2fr_1.2fr_130px_100px_1fr_auto]
                gap-2 items-start
            "
        >
            <div className="min-w-0">
                <p className="text-xs font-medium opacity-60">Raw class</p>
                <p className="text-sm font-semibold break-words">
                    {correction.raw_class || "-"}
                </p>
            </div>

            <div className="min-w-0">
                <p className="text-xs font-medium opacity-60">Raw type</p>
                <p className="text-sm font-semibold break-words">
                    {correction.raw_type || "-"}
                </p>
            </div>

            <label className="space-y-1 text-xs">
                <span className="font-medium opacity-60">Canonical class</span>
                <input
                    value={toInputValue(form.canonical_class)}
                    onChange={(e) => updateField("canonical_class", e.target.value)}
                    className="
                        w-full p-1.5 rounded-md text-sm
                        border border-border dark:border-borderDark
                        bg-background dark:bg-backgroundDark
                    "
                />
            </label>

            <label className="space-y-1 text-xs">
                <span className="font-medium opacity-60">Canonical type</span>
                <input
                    value={toInputValue(form.canonical_type)}
                    onChange={(e) => updateField("canonical_type", e.target.value)}
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
