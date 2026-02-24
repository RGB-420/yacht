import pandas as pd
import re

def list_to_csv_cell(values):
    if isinstance(values, list):
        return ", ".join(values)
    return values

def upper_class_list(values):
    if not isinstance(values, list):
        return values
    return [v for v in values if isinstance(v, str)]

def fill_empty_class(row):
    classes = row.get("Class", [])
    boat_types = row.get("Boat Type", [])

    if not isinstance(classes, list):
        classes = []

    if not isinstance(boat_types, list):
        boat_types = []

    if len(classes) == 0:
        return boat_types

    return classes