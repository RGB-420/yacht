from app.services.normalizers import owners, name, boat_id, clubs, type_class

from app.services.aggregation.boats import group_boats
from app.services.aggregation.aggregation import aggregate_boat_groups

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

final_columns = ["Name", "Class", "Boat Type", "Owner", "Boat Id", "Club", "Source"]

def log_df_stats(df, step):
    logger.info(f"[{step}] Rows: {len(df)}")

    if "Name" in df.columns:
        logger.info(f"[{step}] Unique boats: {df['Name'].nunique()}")

    if "Boat Id" in df.columns:
        logger.info(f"[{step}] Boat Ids null: {df['Boat Id'].isna().sum()}")


def generate_master_boats(df):
    log_df_stats(df, "INITIAL")

    df = owners.finalize_owner_column(df)
    log_df_stats(df, "OWNERS")

    df = name.finalize_name_column(df)
    log_df_stats(df, "NAME")
    
    df = boat_id.finalize_boat_id_column(df)
    log_df_stats(df, "BOAT_ID")

    df = type_class.final_type_class_columns(df)
    log_df_stats(df, "TYPE_CLASS")
    
    df = clubs.finalize_club_column(df)
    log_df_stats(df, "CLUBS")

    df = group_boats(df)
    log_df_stats(df, "GROUP_BOATS")

    df = aggregate_boat_groups(df, final_columns)
    log_df_stats(df, "AGGREGATE")

    df[final_columns].to_csv("data/processed/boats_normalized.csv")
    
    return df[final_columns]
