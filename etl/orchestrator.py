from etl.pipelines.scrape_pipelines import run_scrape_pipeline
from etl.pipelines.master_boats_pipeline import run_master_boats_pipeline
from etl.pipelines.regattas_pipeline import run_regattas_pipeline
from etl.pipelines.classes_pipeline import run_classes_pipeline

def run_full_pipeline():
    print("Starting full pipeline...")

    #run_scrape_pipeline()
    #run_master_boats_pipeline()
    #run_regattas_pipeline()
    run_classes_pipeline()

    print("Pipeline finished succesfully")