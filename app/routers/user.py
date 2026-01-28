from fastapi import FastAPI,HTTPException,status,Response,Depends,APIRouter
from app import models,schemas,utils
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List

router = APIRouter()


@router.post("/users" , status_code=status.HTTP_201_CREATED , response_model=schemas.UserRes)
def rafikul_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
      if db.query(models.User).filter(models.User.email == user.email).first():
            raise HTTPException (400, "Email already exist")
      hashed_password  = utils.hash_password(user.password)
      user.password =  hashed_password
      new_user = models.User(**user.model_dump())
      db.add(new_user)
      db.commit()
      db.refresh(new_user)
      return new_user