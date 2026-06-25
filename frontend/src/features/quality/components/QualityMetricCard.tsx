import type { CoverageMetric } from "../types"

type Props = {
    metric: CoverageMetric
}

export const QualityMetricCard = ({ metric }: Props) => {
    return (
        <div
            className="
                p-4 rounded-xl
                border border-border dark:border-borderDark
                bg-background dark:bg-backgroundDark
                space-y-3
            "
        >
            <div className="flex justify-between gap-3">
                <div>
                    <p className="font-semibold">{metric.label}</p>
                    <p className="text-sm opacity-70">
                        {metric.covered} of {metric.total} covered
                    </p>
                </div>

                <div className="text-right">
                    <p className="text-xl font-bold">
                        {metric.coverage_pct}%
                    </p>
                    <p className="text-xs opacity-60">
                        {metric.missing} missing
                    </p>
                </div>
            </div>

            <div className="h-2 rounded-full bg-border dark:bg-borderDark overflow-hidden">
                <div
                    className="h-full bg-primary dark:bg-primaryDark rounded-full"
                    style={{ width: `${metric.coverage_pct}%` }}
                />
            </div>
        </div>
    )
}
