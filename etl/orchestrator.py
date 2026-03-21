from etl.pipelines.scrape_pipelines import run_scrape_pipeline
from etl.pipelines.boats_pipeline import run_boats_pipeline
from etl.pipelines.classes_pipeline import run_classes_pipeline
from etl.pipelines.clubs_pipeline import run_clubs_pipeline
from etl.pipelines.regattas_pipeline import run_regattas_pipeline

def run_full_pipeline():
    print("Starting full pipeline...")

    #run_scrape_pipeline()
    #run_boats_pipeline()
    #run_regattas_pipeline()
    #run_classes_pipeline()
    run_clubs_pipeline()

    print("Pipeline finished succesfully")