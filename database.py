from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker




# Update with your actual PostgreSQL credentials
DATABASE_URL = "postgresql://postgres:test1234@localhost:5432/musicapp"

engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

# dependency injection

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()