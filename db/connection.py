import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    user = os.getenv("DB_USER")
    password= os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME")

    if not all([user, password, host, port, database]):
        raise ValueError("Database credentials not properly set in enviroment variables")
    
    url = URL.create(
            drivername="postgresql+psycopg2",
            username=user,
            password=password,
            host=host,
            port=port,
            database=database,
        )

    engine = create_engine(url, echo=False, future=True, pool_pre_ping=True, connect_args={"sslmode": "require"})

    return engine
