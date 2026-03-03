from domain.normalizers import owners, name, boat_id, clubs, type_class

from domain.grouping.boats import group_boats
from domain.grouping.aggregation import aggregate_boat_groups

final_columns = ["Name", "Class", "Boat Type", "Owner", "Boat Id", "Club", "Source", "Year"]

def generate_master_boats(df):
    df = owners.finalize_owner_column(df)
    df = name.finalize_name_column(df)
    df = boat_id.finalize_boat_id_column(df)
    df = type_class.final_type_class_columns(df)
    df = clubs.finalize_club_column(df)

    df = group_boats(df)

    df = aggregate_boat_groups(df, final_columns)

    return df[final_columns]
