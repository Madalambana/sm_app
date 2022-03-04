from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import encrytion, models, schemas
from ..database import get_db

router = APIRouter(
    tags=["Sign up"]
)

@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
def sign_up(postman: schemas.Signup,db: Session = Depends(get_db)):
    usernameQuery = db.query(models.Users).filter(models.Users.username == postman.username).first()
    studentnrQuery = db.query(models.Users).filter(models.Users.studentnr == postman.studentnr).first()
    if usernameQuery:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exits")
    if studentnrQuery:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="ID already exits")
    password = encrytion.encrypt(postman.password)
    postman.password = password
    newUser = models.Users(**postman.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    
    return {"Welcome aboard user:" : postman.username}

