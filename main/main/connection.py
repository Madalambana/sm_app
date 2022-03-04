from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, login, likes, signup
from . import models
from sqlalchemy import engine
from .database import engine
from starlette.responses import RedirectResponse
import time

try:
    models.Base.metadata.create_all(bind=engine)
    print("Successfully Connected")
except Exception as error:
    print('error', error)


app = FastAPI()
app.include_router(signup.router)
app.include_router(post.router)
app.include_router(login.router)


origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_308_PERMANENT_REDIRECT)
def main():
    correctPage = RedirectResponse("/login")
    return correctPage