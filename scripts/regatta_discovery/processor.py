

def normalize_text(result):
    normalize_result = (result["title"] + " " + result["snippet"]).lower()
    return normalize_result

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

def filter_results(results):
    filtered = []

    for r in results:
        print("\n---")
        print("TITLE:", r["title"])

        if is_relevant_result(r):
            print("- Relevant")
        else:
            print("- NOT Relevant")

        if is_noise(r):
            print("- Noise")
        
        if is_relevant_result(r) and not is_noise(r):
            print("KEPT")
            filtered.append(r)
        else:
            print("REMOVED")

    return filtered