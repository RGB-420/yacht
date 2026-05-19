import argparse
import time
import sys

from pipelines.scraping.scrape_pipelines import run_scrape_pipeline
from pipelines.boats.boats_pipeline import run_boats_pipeline
from pipelines.classes.classes_pipeline import run_classes_pipeline
from pipelines.clubs.clubs_pipeline import run_clubs_pipeline
from pipelines.regattas.regattas_pipeline import run_regattas_pipeline

from pipelines.orchestrator import run_full_pipeline

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

PIPELINES = {
    "scrape": run_scrape_pipeline,
    "boats": run_boats_pipeline,
    "classes": run_classes_pipeline,
    "clubs": run_clubs_pipeline,
    "regattas": run_regattas_pipeline,
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
            logger.exception(f"Pipeline failed: {e}")

            sys.exit(1)

        end = time.time()

        logger.info(f"Finished in {end - start:.2f} seconds")


if __name__ == "__main__":
    main()