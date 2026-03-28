from datetime import datetime, timedelta, timezone
from pathlib import Path

CALENDAR_FILE_PATH = Path("data/regattas_calendar.ics")

def generate_ics(events):
    with open(CALENDAR_FILE_PATH, "w", encoding="utf-8") as f:
        f.write("BEGIN:VCALENDAR\n")
        f.write("VERSION:2.0\n")

        for e in events:
            start = e["start_date"]
            end = e["end_date"]

            if not start or not end:
                continue

            now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

            summary = f"{e['name']} {e['year']}".replace(",", "")
            end_date = end + timedelta(days=1)

            f.write("BEGIN:VEVENT\n")

            f.write(f"UID:{e['name']}-{e['year']}@regattas\n")
            f.write(f"DTSTAMP:{now}\n")

            f.write(f"SUMMARY:{summary}\n")            

            f.write(f"DTSTART:{start.strftime('%Y%m%d')}\n")
            f.write(f"DTEND:{end_date.strftime('%Y%m%d')}\n")

            if e.get("url"):
                f.write(f"DESCRIPTION:{summary}\\nMore info: {e['url']}\n")
            else:
                f.write(f"DESCRIPTION:{summary})\n")

            f.write("END:VEVENT\n")
        
        f.write("END:VCALENDAR\n")