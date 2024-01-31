from passlib.context import CryptContext
from src.db.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")





