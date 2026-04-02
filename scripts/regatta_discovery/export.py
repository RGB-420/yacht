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
                "snippet"
            ])
            
        for r in results:
                    writer.writerow([
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        query,
                        location,
                        r["title"],
                        r["link"],
                        r["snippet"]
                    ])

def save_query_performance(query, total, relevant, filename):
      file_exists = os.path.isfile(filename)

      precision = relevant / total if total > 0 else 0

      with open(filename, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow([
                    "timestamp",
                    "query",
                    "total_results",
                    "relevant_results",
                    "precision"
                ])
            
            writer.writerow([
                  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  query,
                  total,
                  relevant,
                  round(precision, 2)
            ])