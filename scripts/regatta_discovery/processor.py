def normalize_text(result):
    normalize_result = (result["title"] + " " + result["snippet"]).lower()
    return normalize_result

def score_result(result):
    text = normalize_text(result)
    link = result.get("link", "").lower()

    score = 0

    # 🟢 señales fuertes
    if "regatta" in text:
        score += 3
    if "championship" in text:
        score += 3
    if "cup" in text or "trophy" in text:
        score += 2

    if "overall" in text:
        score += 3
    if "final results" in text:
        score += 3
    if "race results" in text:
        score += 2
    if "full results" in text:
        score += 2
    if "results -" in text:
        score += 2

    if "race 1" in text or "race 2" in text:
        score += 2
    if "series results" in text:
        score += 2    
        
    # 🟡 señales útiles
    if "results" in text or "resultados" in text or "risultati" in text:
        score += 1
    if len(result.get("snippet", "")) > 120:
        score += 1

    # 🔴 penalizaciones
    if "archive" in text:
        score -= 2
    if "home" in text:
        score -= 2
    if "club" in text:
        score -= 1
    if "youtube" in text:
        score -= 3

    position = result.get("position")

    if position is not None:
        score += max(0, 5 - (position / 4))

    return score


def deduplicate_results(results):
    seen_links = set()
    unique = []

    for r in results:
        if r["link"] not in seen_links:
            unique.append(r)
            seen_links.add(r["link"])

    return unique

def filter_results(results):
    filtered = []

    for r in results:
        score = score_result(r)
        r["score"] = score

        print(f"Score: {score}")

        if score >= 6:
            filtered.append(r)

    filtered = deduplicate_results(filtered)

    filtered.sort(key=lambda x: x["score"], reverse=True)

    return filtered