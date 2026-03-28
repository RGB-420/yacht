from pipelines.scraping.scrape_pipelines import run_scrape_pipeline
from pipelines.boats.boats_pipeline import run_boats_pipeline
from pipelines.classes.classes_pipeline import run_classes_pipeline
from pipelines.clubs.clubs_pipeline import run_clubs_pipeline
from pipelines.regattas.regattas_pipeline import run_regattas_pipeline
from pipelines.schedule.schedule_pipeline import run_scheduled_pipeline

def run_full_pipeline():
    print("Starting full pipeline...")

    run_scrape_pipeline()
    run_boats_pipeline()
    run_regattas_pipeline()
    run_classes_pipeline()
    run_clubs_pipeline()
    run_scheduled_pipeline()

    print("Pipeline finished succesfully")