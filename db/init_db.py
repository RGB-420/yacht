from db.connection import engine

def init_db():
    with open("db/schema.sql", "r") as f:
        sql = f.read()

    with engine.begin() as conn:
        conn.execute(sql)