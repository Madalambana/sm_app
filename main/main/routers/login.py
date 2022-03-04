from fastapi import Response, HTTPException, Depends, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..encrytion import *
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, encrytion 
from ..oauth2 import create_access_token

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login")
def login(postman:OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.studentnr == postman.username).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not encrytion.compare(postman.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=" Invalid credentials")
    access_token = create_access_token(data={"studentnr": user.studentnr})
    return {"access_token": access_token, "token_type": "bearer"}