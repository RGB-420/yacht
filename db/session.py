from sqlalchemy.orm import sessionmaker

from db.connection import get_engine


engine = get_engine()

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)