from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
import random
from ..oauth2 import current_user
import time 
from ..EV import settings

router = APIRouter(
    tags= ["Comments"]
)

#redirected to this page/ link
@router.post("/comments/{post_id}", status_code=status.HTTP_201_CREATED)
def createComment(postman:schemas.Comment, post_id: int,db: Session = Depends(get_db), current_user: int = Depends(current_user)):
    postqueryPost = db.query(models.Posts).filter(models.Posts.pid == post_id)
    if postqueryPost.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with ID {post_id} does not exist or " + 
        "has been deleted")
    usernameQuery = db.query(models.Users.username).filter(models.Users.studentnr == current_user.studentnr).first()
    usernameQuery = "".join(usernameQuery)
    postqueryComment = models.Comment(username = usernameQuery,p_pid = post_id,**postman.dict())
    db.add(postqueryComment)
    db.commit()
    db.refresh(postqueryComment)
    return {"Successfully commented"}

#redirected to this page/ link
@router.get("/comments_vl70={post_id}", response_model=List[schemas.CommentReturn])
def getComment(post_id: int,db: Session = Depends(get_db), current_user: int = Depends(current_user)):
    commentQuery = db.query(models.Comment).filter(models.Comment.p_pid == post_id).all()
    return commentQuery

    #Comments currently have a table of their own and are not next to the table posts as of yet