import datetime

from sqlalchemy import Column, Integer, String, Sequence, Text, DateTime

from database import Base, engine

from flask.ext.login import UserMixin

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, Sequence("song_id_sequence"), primary_key=True)
    name = Column(String(128))
    email = Column(String(128))
    password = Column(String(128))
    posts = relationship("Post", backref="author")

    def is_authenticated(self):
        return True

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, Sequence("song_id_sequence"), primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)
    author_id = Column(Integer, ForeignKey('users.id'))


# This line must be below your classes or the new classes you create will not create tabels.
Base.metadata.create_all(engine)
