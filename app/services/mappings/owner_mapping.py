from app.services.mappings.loader import load_simple_mapping

owner_mapping = load_simple_mapping("owner_mapping.csv", "raw_name", "canonical_name")