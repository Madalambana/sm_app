from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    tags=["Sign up"]
)

@router("sign_up", status_code=status.HTTP_201_CREATED)
def sign_up (postman: schemas.Signup,db: Session = Depends(get_db)):
    newAccount = models.Post(**postman)
    db.add(newAccount)
    db.commit()
    db.refresh(newAccount)
    return {postman.email: "successfully created"}