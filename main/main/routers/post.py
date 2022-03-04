from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
import random
from ..oauth2 import current_user
import time 
from ..EV import settings

def PID():
    return random.randrange(settings.PID_RANDRAGE)

router = APIRouter(
    tags= ["All Posts"]
)

@router.get("/home", response_model=List[schemas.Return2])
def main(limit = 20, search: Optional[str] = "",db: Session = Depends(get_db), current_user: int = Depends(current_user)):
    post = db.query(models.Posts).limit(limit).all()
    return post

@router.get("/my_posts", response_model=List[schemas.MyPost])
def my_posts(db: Session = Depends(get_db),current_user: int = Depends(current_user)):
    usernameQuery = db.query(models.Users.username).filter(models.Users.studentnr == current_user.studentnr).first()
    usernameQuery = "".join(usernameQuery)
    myPosts = db.query(models.Posts).filter(models.Posts.username == usernameQuery).all()
    return myPosts

@router.post("/new_post", status_code=status.HTTP_201_CREATED,)
def new_post(postman: schemas.Post ,db: Session = Depends(get_db),current_user: int = Depends(current_user)):
    pidNr = PID()
    pidQuery = db.query(models.Posts).filter(models.Posts.pid == pidNr).first()
    usernameQuery = db.query(models.Users.username).filter(models.Users.studentnr == current_user.studentnr).first()
    usernameQuery = "".join(usernameQuery)
    if pidQuery == pidNr:
        time.sleep(2)
        pidNr = PID()
    newPost = models.Posts(pid = pidNr,username = usernameQuery,**postman.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost

@router.delete("/purge/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int,db: Session = Depends(get_db), current_user: int = Depends(current_user)):
    username1 = db.query(models.Users.username).filter(models.Users.studentnr == current_user.studentnr).first()
    username1 = "".join(username1)
    username2  = db.query(models.Posts.username).filter(models.Posts.pid == post_id).first()
    if username1 == username2:
        deletedPost = db.query(models.Posts).filter(models.Posts.pid == post_id)
        if deletedPost.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        deletedPost.delete(synchronize_session=False)
        db.commit()
        return "Successfully deleted"
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unauthorized")

@router.put("/overhaul/{post_id}", response_model=schemas.Return2)
def update_post(postman:schemas.Update ,post_id: int,db: Session = Depends(get_db), current_user: int = Depends(current_user)):
    username1 = db.query(models.Users.username).filter(models.Users.studentnr == current_user.studentnr).first()
    username1 = "".join(username1)
    username2  = db.query(models.Posts.username).filter(models.Posts.pid == post_id).first()
    if username1 == username2:
        updatedPost = db.query(models.Posts).filter(models.Posts.pid == post_id)
        if updatedPost.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post is non-existant")
        updatedPost.update(postman.dict(),synchronize_session=False)
        db.commit()
        return updatedPost.first()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unauthorized")