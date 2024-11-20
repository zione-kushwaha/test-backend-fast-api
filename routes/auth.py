import uuid
import bcrypt
from database import get_db
from models.users import User
from pydantic_schemas.user_create import UserCreate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from pydantic_schemas.user_login import UserLogin

router = APIRouter()



@router.post("/signup/", status_code=201)
def signup(user: UserCreate, db= Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:

        #raise http exception
        raise HTTPException(status_code=400, detail="Email already registered==")
    
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(id=str(uuid.uuid4()), name=user.name, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login/")
def login_user(user: UserLogin,db: Session = Depends(get_db)):
  # checking if a user with same email exists already  or not
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    if not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    return db_user