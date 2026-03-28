from app.services.mappings.loader import load_regex_grouped_mapping

class_mapping = load_regex_grouped_mapping("class_mapping.csv", "pattern", "canonical_name")