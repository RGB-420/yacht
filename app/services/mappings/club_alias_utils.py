def group_resolved_aliases(rows):
    grouped = {}

    for row in rows:
        key = (row["raw_name"], row["normalized_name"])

        if key not in grouped:
            grouped[key] = {
                "raw_name": row["raw_name"], 
                "normalized_name": row["normalized_name"], 
                "canonical_names": []}

        grouped[key]["canonical_names"].append(row["canonical_name"])

    result = []

    for item in grouped.values():
        result.append({
            "raw_name": item["raw_name"], 
            "normalized_name": item["normalized_name"], 
            "canonical_name": " // ".join(sorted(set(item["canonical_names"])))
        })

    return result

def group_club_alias_cache(rows):
    grouped = {}

    for row in rows:
        key = row["id_alias"]

        if key not in grouped:
            grouped[key] = {
                "id_alias": row["id_alias"],
                "raw_name": row["raw_name"],
                "normalized_name": row["normalized_name"],
                "status": row["status"],
                "confidence": row["confidence"],
                "canonical_names": []
            }
        
        if row["canonical_name"]:
            grouped[key]["canonical_names"].append(row["canonical_name"])

    result = []

    for item in grouped.values():
        result.append({
            "id_alias": item["id_alias"],
            "raw_name": item["raw_name"],
            "normalized_name": item["normalized_name"],
            "status": item["status"],
            "confidence": item["confidence"],
            "canonical_name": " // ".join(sorted(set(item["canonical_names"])))
        })

    return result

def group_club_mappings(rows):
    grouped = {}

    for row in rows:
        key = row["id_alias"]

        if key not in grouped:
            grouped[key] = {
                "id_alias": row["id_alias"],
                "raw_name": row["raw_name"],
                "normalized_name": row["normalized_name"],
                "status": row["status"],
                "confidence": row["confidence"],
                "alias_type": row["alias_type"],
                "notes": row["notes"],

                "country": row["country"],
                "website": row["website"],
                "entity_type": row["entity_type"],

                "canonical_names": []
            }

        if row["canonical_name"]:
            grouped[key]["canonical_names"].append(row["canonical_name"])

    result = []

    for item in grouped.values():
        result.append({
            "id_alias": item["id_alias"],
            "raw_name": item["raw_name"],
            "normalized_name": item["normalized_name"],
            "status": item["status"],
            "confidence": item["confidence"],
            "alias_type": item["alias_type"],
            "notes": item["notes"],

            "country": item["country"],
            "website": item["website"],
            "entity_type": item["entity_type"],

            "canonical_name": " // ".join(sorted(set(item["canonical_names"])))
        })
    
    return result