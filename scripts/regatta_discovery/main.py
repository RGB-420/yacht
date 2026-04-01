from queries import get_queries_to_run
from serpapi_client import search_google, extract_organic_results
from processor import filter_results
from export import save_results, save_query_performance

QUERIES_PATH = "scripts/regatta_discovery/queries.csv"
MAX_PRIORITY = 1
LIMIT_QUERIES = 1

RESULTS_PATH = "scripts/regatta_discovery/results.csv"

PERFORMANCE_PATH = "scripts/regatta_discovery/query_performance.csv"

def main():
    queries = get_queries_to_run(QUERIES_PATH, MAX_PRIORITY, LIMIT_QUERIES)

    if not queries:
        print("No queries found")
        return
    
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

        save_query_performance(q["query"], total=len(results), relevant=len(filtered), filename=PERFORMANCE_PATH)


if __name__ == "__main__":
    main()