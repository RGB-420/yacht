import csv
import os

from datetime import datetime

def save_results(results, query, location, filename):
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "query",
                "location",
                "title",
                "link",
                "snippet",
                "score"
            ])
            
        for r in results:
                    writer.writerow([
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        query,
                        location,
                        r["title"],
                        r["link"],
                        r["snippet"],
                        r.get("score", 0)
                    ])

def save_query_performance(query, total, results, filename):
    file_exists = os.path.isfile(filename)

    relevant = len(results)

    precision = relevant / total if total > 0 else 0

    avg_score = sum(r["score"] for r in results) / relevant if relevant > 0 else 0
    max_score = max((r["score"] for r in results), default=0)

    with open(filename, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "query",
                "total_results",
                "kept_results",
                "precision",
                "avg_score",
                "max_score"
            ])
        
        writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                query,
                total,
                relevant,
                round(precision, 2),
                round(avg_score, 2),
                max_score
        ])