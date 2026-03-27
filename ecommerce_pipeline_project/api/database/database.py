import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

ANALYTICS_DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('ANALYTICS_DB_USER', 'postgres')}"
    f":{os.getenv('ANALYTICS_DB_PASSWORD', '123')}"
    f"@{os.getenv('ANALYTICS_DB_HOST', 'localhost')}"
    f":{os.getenv('ANALYTICS_DB_PORT', '5432')}"
    f"/{os.getenv('ANALYTICS_DB_NAME', 'analytics')}"
)

engine = create_engine(ANALYTICS_DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
