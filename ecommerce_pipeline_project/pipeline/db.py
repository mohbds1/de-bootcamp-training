import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Function to build connection string for PostgreSQL
def build_postgres_url(prefix):
    host = os.getenv(f"{prefix}_HOST", "localhost")
    port = os.getenv(f"{prefix}_PORT", "5432")
    db = os.getenv(f"{prefix}_NAME")
    user = os.getenv(f"{prefix}_USER", "postgres")
    password = os.getenv(f"{prefix}_PASSWORD", "123")

    if not db:
        raise ValueError(f"Missing database name for prefix {prefix}")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


raw_engine = create_engine(build_postgres_url("RAW_DB"), future=True)
analytics_engine = create_engine(build_postgres_url("ANALYTICS_DB"), future=True)
