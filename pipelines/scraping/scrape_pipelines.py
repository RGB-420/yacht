from scraping.runner import scrape_web, scrape_pdfs

def run_scrape_pipeline():
    print("Running web scraper...")
    scrape_web()

    print("Running PDF scrapers...")
    scrape_pdfs()