from jose import JWTError, jwt 
from datetime import datetime,timedelta
from . import schemas, models
from .EV import settings
from .database import get_db
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#secret_key
#algorithm
#expiration time

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        studentnr = payload.get("studentnr")

        if studentnr == None:
            raise credentials_exception
        token_data = schemas.Token_data(studentnr=studentnr)
    except JWTError:
        raise credentials_exception
    return token_data

def current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,detail= 
            "Cannot authenticate", headers={"WWW-Authenticate": "Bearer"})
    token = verify_token(token,credentials_exception)
    user = db.query(models.Users).filter(models.Users.studentnr == token.studentnr).first()
    return user

