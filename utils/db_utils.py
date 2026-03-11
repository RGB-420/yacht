def rows_to_dict(result):
    return [dict(row._mapping) for row in result]

def row_to_dict(row):
    if row:
        return dict(row._mapping)
    return None