import pandas as pd
import re

from app.services.normalizers.owners import split_and_dedupe

from app.core.config import DATA_DEBUG

DEBUG_PATH = DATA_DEBUG / "owner_raw_debug.csv"

OUTPUT_PATH = DATA_DEBUG / "owner_source_analysis.csv"

COMPANY_KEYWORDS = ["LTD", "LLP", "LIMITED", "PARTNERS", "PARTNER", "CAPITAL", "SERVICES", "SERVICE", "ASSOCIATION", "ASSOCIATES", "ACADEMY", "PROJECT", "GROUP", "INVEST"]

CLUB_KEYWORDS = ["CLUB", "RACING"]

def analyze_owner_sources():
    df = pd.read_csv(DEBUG_PATH)

    rows = []

    for source, group in df.groupby("source"):
        owners = (group["raw_owner"].dropna().drop_duplicates().tolist())

        owner_count = len(owners)

        one_token = 0
        two_tokens = 0
        three_tokens = 0
        four_plus_tokens = 0

        multi_owner_count = 0
        company_count = 0
        club_count = 0
        contains_number_count = 0
        invalid_owner_count = 0

        total_tokens = 0

        split_owners = []

        for owner in owners:
            parts = split_and_dedupe(owner)

            if isinstance(parts, list):
                split_owners.extend(parts)

            elif pd.notna(parts):
                split_owners.append(parts)

        split_owner_count = len(split_owners)

        for owner in split_owners:
            token_count = count_tokens(owner)

            total_tokens += token_count

            if token_count == 1:
                one_token += 1

            elif token_count == 2:
                two_tokens += 1

            elif token_count == 3:
                three_tokens += 1

            else:
                four_plus_tokens += 1
            
            if is_company(owner):
                company_count += 1

            if is_club(owner):
                club_count += 1

        for owner in owners:
            if is_multi_owner(owner):
                multi_owner_count += 1
            
            if contains_number(owner):
                contains_number_count += 1
            
            if is_invalid(owner):
                invalid_owner_count += 1

        avg_tokens = (round(total_tokens / split_owner_count, 2) if split_owner_count else 0)

        owner_expansion_ratio = (round(split_owner_count / owner_count, 2) if owner_count else 0)

        samples = owners[:10]

        rows.append({
            "source": source,

            "raw_owner_count": owner_count,
            "split_owner_count": split_owner_count,

            "owner_expansion_ratio": owner_expansion_ratio,

            "avg_tokens": avg_tokens,

            "owners_1_token": one_token,
            "owners_2_token": two_tokens,
            "owners_3_token": three_tokens,
            "owners_4plus_token": four_plus_tokens,

            "multi_owner_count": multi_owner_count,

            "company_count": company_count,
            "club_count": club_count,

            "contains_number_count": contains_number_count,
            "invalid_owner_count": invalid_owner_count,

            "sample_1": samples[0] if len(samples) > 0 else "",
            "sample_2": samples[1] if len(samples) > 1 else "",
            "sample_3": samples[2] if len(samples) > 2 else "",
            "sample_4": samples[3] if len(samples) > 3 else "",
            "sample_5": samples[4] if len(samples) > 4 else "",
            "sample_6": samples[5] if len(samples) > 5 else "",
            "sample_7": samples[6] if len(samples) > 6 else "",
            "sample_8": samples[7] if len(samples) > 7 else "",
            "sample_9": samples[8] if len(samples) > 8 else "",
            "sample_10": samples[9] if len(samples) > 9 else "",
        })

    result = pd.DataFrame(rows)

    result = result.sort_values(by="raw_owner_count", ascending=False)

    result.to_csv(OUTPUT_PATH, index=False)

    print(f"Exported {len(result)} sources -> {OUTPUT_PATH}")

def count_tokens(owner):
    return len(str(owner).split())

def is_multi_owner(owner):
    owner = str(owner).upper()

    return any(sep in owner for sep in [" & ", " AND ", " ET ", "/"])

def is_company(owner):
    owner = str(owner).upper()

    return any(keyword in owner for keyword in COMPANY_KEYWORDS)

def is_club(owner):
    owner = str(owner).upper()

    return any(keyword in owner for keyword in CLUB_KEYWORDS)

def contains_number(owner):
    return bool(re.search(r"\d", str(owner)))

def has_letter(owner):
    return bool(re.search(r"[A-Za-z]", str(owner)))

def is_invalid(owner):
    owner = str(owner).strip()

    if not owner:
        return True
    
    if not has_letter(owner):
        return True
    
    return False

if __name__ == "__main__":
    analyze_owner_sources()