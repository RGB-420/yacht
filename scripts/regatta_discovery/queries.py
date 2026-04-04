import csv

def load_queries(path):
    queries = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["full_location"] = f"{row['location']}, {row['country']}"
            queries.append(row)

    return queries

def filter_active_queries(queries):
    filtered_queries = [q for q in queries if q["active"] == "1"]
    return filtered_queries

def filter_by_priority(queries, max_priority):
    filtered_queries = [q for q in queries if int(q["priority"]) <= max_priority]
    return filtered_queries

def get_queries_to_run(path, max_priority):
    queries = load_queries(path)
    queries = filter_active_queries(queries)
    queries = filter_by_priority(queries, max_priority)

    return queries