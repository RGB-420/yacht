from app.services.mappings.loader import load_simple_mapping

owner_mapping = load_simple_mapping("owner_mapping.csv", "owner_raw_name", "owner_canonical_name")