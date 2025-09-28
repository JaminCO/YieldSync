from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)


try:
    # DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app/data/support_db.sqlite3")
    # DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@localhost/support_db")

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    print(f"DATABASE_CONNECTION_ERROR: {str(e)} - database_initialization")
    raise e

def get_db():
    try:
        # Create a new session
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    except Exception as e:
        print(f"DATABASE_CONNECTION_ERROR: {str(e)} - get_db")
        raise e