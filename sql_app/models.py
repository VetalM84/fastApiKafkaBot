"""Models for SQLAlchemy."""

from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime, text
from sqlalchemy.orm import relationship

from .database import Base

sent_log = Table(
    "sent_log",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("article_id", ForeignKey("articles.id"), primary_key=True),
    Column('sent_time', DateTime(), server_default=text('NOW()')),
)


class User(Base):
    """User model. Has Many2Many relationship with Article."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String(50))
    pet_name = Column(String(50))
    language_code = Column(String(5))

    sent_articles = relationship(
        "Article", secondary=sent_log, back_populates="sent_to_user"
    )


class Article(Base):
    """Article model. Has Many2Many relationship with User."""

    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1024))
    image_url = Column(String(500))
    language_code = Column(String(255), index=True)

    sent_to_user = relationship(
        "User", secondary=sent_log, back_populates="sent_articles"
    )


# class Log(Base):
#     __tablename__ = "sent_log"
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     recipient = relationship("User", back_populates="sent_items")
#
#     article_id = Column(Integer, ForeignKey("articles.id"))
#     article = relationship("Article", back_populates="items")
