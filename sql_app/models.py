from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String(50))
    pet_name = Column(String(50))
    language_code = Column(String(5))

    sent_items = relationship("Log", back_populates="recipient")


class Log(Base):
    __tablename__ = "sent_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recipient = relationship("User", back_populates="sent_items")

    article_id = Column(Integer, ForeignKey("articles.id"))
    article = relationship("Article", back_populates="items")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1024))
    image_url = Column(String(500))
    language_code = Column(String(255), index=True)

    items = relationship("Log", back_populates="article")
