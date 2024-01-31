from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from src.db.operations.user_crud import create_user, get_user_by_email
from src.schemas.user import UserCreate, UserInDB
from src.db.utils import get_db, pwd_context
from src.db.jwt import get_current_user, create_access_token, Token

router = APIRouter()

@router.post("/register", response_model=UserInDB)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)


@router.post("/login", response_model=Token)
async def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    print(db_user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserInDB)
async def me(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_user = get_user_by_email(db, current_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user