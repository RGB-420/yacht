import random

from regatta_discovery.queries import get_queries_to_run
from regatta_discovery.serpapi_client import search_google, extract_organic_results
from regatta_discovery.processor import filter_results
from regatta_discovery.export import save_results, save_query_performance

QUERIES_PATH = "data/regatta_discovery/queries.csv"
MAX_PRIORITY = 1
LIMIT_QUERIES = 2

RESULTS_PATH = "data/regatta_discovery/results.csv"
RAW_RESULTS_PATH = "data/regatta_discovery/raw_results.csv"

PERFORMANCE_PATH = "data/regatta_discovery/query_performance.csv"

def main():
    all_queries = get_queries_to_run(QUERIES_PATH, MAX_PRIORITY)

    if not all_queries:
        print("No queries found")
        return
    
    queries = random.sample(all_queries, min(LIMIT_QUERIES, len(all_queries)))

    for q in queries:
        print(f" Query: {q['query']}")
        print(f" Location: {q['full_location']}")

        response = search_google(q["query"], q["full_location"])

        results = extract_organic_results(response)

        filtered = filter_results(results)

        print(f"Total results: {len(results)}")
        print(f"Filtered results: {len(filtered)}")

        if not filtered:
            print("No relevant results found")

        save_results(filtered, q["query"], q["full_location"], RESULTS_PATH)

        save_results(results, q["query"], q["full_location"], RAW_RESULTS_PATH)

        save_query_performance(q["query"], total=len(results), results=filtered, filename=PERFORMANCE_PATH)


if __name__ == "__main__":
    main()