import random

from queries import get_queries_to_run
from serpapi_client import search_google, extract_organic_results
from processor import filter_results
from export import save_results, save_query_performance

QUERIES_PATH = "scripts/regatta_discovery/queries.csv"
MAX_PRIORITY = 1
LIMIT_QUERIES = 2

RESULTS_PATH = "scripts/regatta_discovery/results.csv"
RAW_RESULTS_PATH = "scripts/regatta_discovery/raw_results.csv"

PERFORMANCE_PATH = "scripts/regatta_discovery/query_performance.csv"

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