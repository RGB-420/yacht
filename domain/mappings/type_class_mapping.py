from domain.mappings.loader import load_dual_mapping

type_class_mapping = load_dual_mapping("type_class_mapping.csv", ["raw_class", "raw_type"], ["canonical_class", "canonical_type"])