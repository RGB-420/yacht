def normalize_text(result):
    normalize_result = (result["title"] + " " + result["snippet"]).lower()
    return normalize_result

def score_result(result):
    text = normalize_text(result)

    score = 0

    # 🟢 señales fuertes
    if "regatta" in text:
        score += 3
    if "championship" in text:
        score += 3
    if "cup" in text or "trophy" in text:
        score += 2

    # 🟡 señales útiles
    if "results" in text or "resultados" in text or "risultati" in text:
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

    return score

def is_relevant_result(result):
    text = normalize_text(result)

    keywords = [
        "regatta",
        "sailing",
        "vela",
        "yacht",
        "club",
        "race",
        "results",
        "resultados",
        "risultati",
        "resultats"
    ]

    return any(k in text for k in keywords)

def is_noise(result):
    text = normalize_text(result)

    noise_keywords = [
        "weather",
        "clothing",
        "sale",
        "shop",
        "festival",
        "history",
        "what is",
        "guide",
        "tourism"
    ]

    return any(k in text for k in noise_keywords)

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
        print("\n---")
        print("TITLE:", r["title"])

        score = score_result(r)
        r["score"] = score

        print(f"Score: {score}")

        if score >= 2:
            print("KEPT")
            filtered.append(r)
        else:
            print("REMOVED")

    filtered = deduplicate_results(filtered)

    filtered.sort(key=lambda x: x["score"], reverse=True)

    return filtered