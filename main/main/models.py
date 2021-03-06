from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean
from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, column
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Posts(Base):
    __tablename__ = "posts"
    username = Column(String,ForeignKey('users.username', ondelete="CASCADE"), nullable=False,)
    pid = Column(Integer, primary_key=True, nullable=False)
    post = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))

class Users(Base):
    __tablename__ = "users"
    username = Column(String, nullable=False, primary_key=True)
    studentnr = Column(Integer, nullable=False, unique=True)
    password = Column(String, nullable=False,)

class Comment(Base):
    __tablename__ = "comments"
    p_pid = Column(Integer, nullable=False)
    username = Column(String, nullable=False,)
    comment = Column(String,primary_key= True, nullable=False)