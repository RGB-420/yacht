import argparse
import time

from etl.pipelines.scrape_pipelines import run_scrape_pipeline
from etl.pipelines.boats_pipeline import run_boats_pipeline
from etl.pipelines.classes_pipeline import run_classes_pipeline
from etl.pipelines.clubs_pipeline import run_clubs_pipeline
from etl.pipelines.regattas_pipeline import run_regattas_pipeline
from etl.pipelines.schedule_pipeline import run_scheduled_pipeline

from etl.orchestrator import run_full_pipeline


PIPELINES = {
    "scrape": run_scrape_pipeline,
    "boats": run_boats_pipeline,
    "classes": run_classes_pipeline,
    "clubs": run_clubs_pipeline,
    "regattas": run_regattas_pipeline,
    "schedule": run_scheduled_pipeline,
    "full": run_full_pipeline,
}


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline CLI - Run ETL pipelines"
    )

    parser.add_argument(
        "command",
        choices=["run"],
        help="Command to execute"
    )

    parser.add_argument(
        "pipeline",
        choices=PIPELINES.keys(),
        help="Pipeline to run"
    )

    args = parser.parse_args()

    if args.command == "run":
        pipeline_name = args.pipeline

        start = time.time()

        try:
            PIPELINES[pipeline_name]()

        except Exception as e:
            print(f"\n❌ Pipeline failed: {e}")

        end = time.time()

        print(f"\nFinished in {end - start:.2f} seconds")


if __name__ == "__main__":
    main()