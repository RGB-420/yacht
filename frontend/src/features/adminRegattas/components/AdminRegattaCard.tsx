import { ExternalLink } from "lucide-react"
import { useState } from "react"
import type {
    AdminRegattaOptions,
    AdminRegattaQueueItem,
    UpdateAdminRegattaQueueItem
} from "../types"

type Props = {
    regatta: AdminRegattaQueueItem
    options: AdminRegattaOptions
    saving: boolean
    onSave: (sourceId: string, data: UpdateAdminRegattaQueueItem) => void
}

const toInputValue = (value?: string | number | null) => {
    if (value === null || value === undefined) return ""

    return String(value)
}

export const AdminRegattaCard = ({
    regatta,
    options,
    saving,
    onSave
}: Props) => {
    const [open, setOpen] = useState(false)
    const [form, setForm] = useState<UpdateAdminRegattaQueueItem>({
        link: regatta.link || "",
        scraper_name: regatta.scraper_name || "",
        source_type: regatta.source_type || "",
        scrape_active: regatta.scrape_active || 0,
        scrape_status: regatta.scrape_status || "",
        specified_class: regatta.specified_class || "",
        notes: regatta.notes || ""
    })

    const sourceId = regatta.source_id || ""

    const updateField = (
        key: keyof UpdateAdminRegattaQueueItem,
        value: string | number
    ) => {
        setForm((current) => ({
            ...current,
            [key]: value
        }))
    }

    return (
        <div
            className="
                p-4 rounded-xl
                border border-border dark:border-borderDark
                bg-background dark:bg-backgroundDark
                space-y-4
            "
        >
            <div className="space-y-1">
                <div className="flex justify-between gap-3">
                    <div>
                        <h2 className="font-semibold">
                            {regatta.regatta_name}
                        </h2>
                        <p className="text-xs opacity-70">
                            {regatta.source_id} · {regatta.year}
                        </p>
                    </div>

                    <span className="text-xs opacity-70">
                        {regatta.status}
                    </span>
                </div>

                <p className="text-sm opacity-80">
                    {regatta.type}
                    {regatta.start_date && ` · ${regatta.start_date}`}
                    {regatta.end_date && ` to ${regatta.end_date}`}
                </p>

                {(regatta.city || regatta.region || regatta.country) && (
                    <p className="text-xs opacity-70">
                        {[regatta.city, regatta.region, regatta.country]
                            .filter(Boolean)
                            .join(", ")}
                    </p>
                )}
            </div>

            <button
                onClick={() => setOpen(!open)}
                className="
                    text-sm px-3 py-1 rounded-xl
                    border border-border dark:border-borderDark
                    hover:bg-primary hover:text-white
                    transition-colors
                "
            >
                {open ? "Collapse" : "Edit"}
            </button>

            {open && (
                <>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <label className="space-y-1 text-sm">
                            <span className="font-medium">Scraper</span>
                            <select
                                value={toInputValue(form.scraper_name)}
                                onChange={(e) => updateField("scraper_name", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            >
                                <option value="">Select scraper</option>
                                {options.scrapers.map((scraper) => (
                                    <option key={scraper} value={scraper}>
                                        {scraper}
                                    </option>
                                ))}
                            </select>
                        </label>

                        <label className="space-y-1 text-sm">
                            <span className="font-medium">Source type</span>
                            <select
                                value={toInputValue(form.source_type)}
                                onChange={(e) => updateField("source_type", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            >
                                <option value="">Select source type</option>
                                {options.source_types.map((sourceType) => (
                                    <option key={sourceType} value={sourceType}>
                                        {sourceType}
                                    </option>
                                ))}
                            </select>
                        </label>

                        <label className="space-y-1 text-sm">
                            <span className="font-medium">Scrape status</span>
                            <select
                                value={toInputValue(form.scrape_status)}
                                onChange={(e) => updateField("scrape_status", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            >
                                {options.scrape_statuses.map((status) => (
                                    <option key={status || "empty"} value={status}>
                                        {status || "Blank"}
                                    </option>
                                ))}
                            </select>
                        </label>

                        <label className="space-y-1 text-sm">
                            <span className="font-medium">Specified class</span>
                            <input
                                value={toInputValue(form.specified_class)}
                                onChange={(e) => updateField("specified_class", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            />
                        </label>
                    </div>

                    <label className="space-y-1 text-sm block">
                        <span className="font-medium">Link</span>
                        <div className="flex gap-2">
                            <input
                                value={toInputValue(form.link)}
                                onChange={(e) => updateField("link", e.target.value)}
                                className="
                                    w-full p-2 rounded-lg
                                    border border-border dark:border-borderDark
                                    bg-background dark:bg-backgroundDark
                                "
                            />

                            {form.link && (
                                <a
                                    href={form.link}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="
                                        px-3 py-2 rounded-lg
                                        border border-border dark:border-borderDark
                                        hover:bg-primary hover:text-white
                                        transition-colors
                                    "
                                >
                                    <ExternalLink size={18} />
                                </a>
                            )}
                        </div>
                    </label>

                    <label className="space-y-1 text-sm block">
                        <span className="font-medium">Notes</span>
                        <textarea
                            value={toInputValue(form.notes)}
                            onChange={(e) => updateField("notes", e.target.value)}
                            className="
                                w-full p-2 rounded-lg
                                border border-border dark:border-borderDark
                                bg-background dark:bg-backgroundDark
                                min-h-20
                            "
                        />
                    </label>

                    <div className="flex justify-between items-center gap-3">
                        <label className="flex items-center gap-2 text-sm">
                            <input
                                type="checkbox"
                                checked={form.scrape_active === 1}
                                onChange={(e) => updateField("scrape_active", e.target.checked ? 1 : 0)}
                            />
                            <span>Active for scraping</span>
                        </label>

                        <button
                            disabled={saving || !sourceId}
                            onClick={() => onSave(sourceId, form)}
                            className="
                                px-4 py-2 rounded-lg
                                bg-primary dark:bg-primaryDark
                                text-white
                                disabled:opacity-50
                            "
                        >
                            {saving ? "Saving..." : "Save"}
                        </button>
                    </div>
                </>
            )}
        </div>
    )
}
