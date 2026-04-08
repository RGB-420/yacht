from app.services.normalizers import owners, name, boat_id, clubs, type_class

from app.services.aggregation.boats import group_boats
from app.services.aggregation.aggregation import aggregate_boat_groups

final_columns = ["Name", "Class", "Boat Type", "Owner", "Boat Id", "Club", "Source"]

def generate_master_boats(df):
    df = owners.finalize_owner_column(df)
    df = name.finalize_name_column(df)
    df = boat_id.finalize_boat_id_column(df)
    df = type_class.final_type_class_columns(df)
    df = clubs.finalize_club_column(df)

    df = group_boats(df)

    df = aggregate_boat_groups(df, final_columns)

    df[final_columns].to_csv("data/processed/boats_normalized.csv")
    return df[final_columns]
