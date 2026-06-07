import re
import pandas as pd

COMPANY_KEYWORDS = ["LTD", "LLP", "LIMITED", "PARTNERS", "PARTNER", "CAPITAL", "SERVICES", "SERVICE", "ASSOCIATION", "ASSOCIATES", "ACADEMY", "PROJECT", "GROUP", "INVEST"]

CLUB_KEYWORDS = ["YACHT CLUB", "SAILING CLUB", "BOAT CLUB", "SAILING"]

MULTIPLE_OWNER_WORDS = [" AND ", " ET ", " Y ", " & "]

def build_result(canonical_name=None, confidence=0, entity_type="UNKNOWN", notes=""):
    if canonical_name is not None:
        canonical_name = canonical_name.title()

    return {
        "canonical_name": canonical_name,
        "confidence": confidence,
        "entity_type": entity_type,
        "notes": notes
    }

def automap_owner(raw_name):

    if pd.isna(raw_name):
        return build_result(
            confidence=0,
            entity_typ="INVALID",
            notes="Null value"
        )

    name = str(raw_name).strip()

    if not name:
        return build_result(
            confidence=0,
            entity_type="INVALID",
            notes="Empty value"
        )
    
    if re.search(r"\d", name):
        return build_result(
            canonical_name=None,
            confidence=0,
            entity_type="INVALID",
            notes="Contains number"
        )

    upper_name = name.upper()

    if any(word in upper_name for word in MULTIPLE_OWNER_WORDS):
        return build_result(
            canonical_name=name,
            confidence=90,
            entity_type="MULTI_OWNER"
        )

    if any(keyword in upper_name for keyword in CLUB_KEYWORDS):
        return build_result(
            canonical_name=name,
            confidence=100,
            entity_type="CLUB"
        )

    if any(keyword in upper_name for keyword in COMPANY_KEYWORDS):
        return build_result(
            canonical_name=name,
            confidence=95,
            entity_type="COMPANY"
        )

    if "FAMILY" in upper_name:
        return build_result(
            canonical_name=name,
            confidence=95,
            entity_type="FAMILY"
        )

    if re.fullmatch(r"[A-Z]{2,8}", upper_name):
        return build_result(
            canonical_name=name,
            confidence=20,
            entity_type="UNKNOWN",
            notes="Possible abbreviation"
        )

    tokens = name.split()

    if not re.search(r"[A-Za-zÀ-ÿ]", name):
        return build_result(
            canonical_name=None,
            confidence=0,
            entity_type="INVALID",
            notes="No letters"
        )

    # Persona simple
    if 2 <= len(tokens) <= 8:
        return build_result(
            canonical_name=name,
            confidence=100,
            entity_type="PERSON"
        )
    
    if len(tokens) == 1:
        return build_result(
            canonical_name=name,
            confidence=40,
            entity_type="UNKNOWN",
            notes="Single token"
        )

    return build_result(
        canonical_name=name,
        confidence=0,
        entity_type="UNKNOWN",
        notes="No rule matched"
    )