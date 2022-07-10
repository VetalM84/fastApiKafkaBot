"""Functions to create, read, update, and delete data from the database."""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import schemas
from db import models


def get_user(db: Session, user_telegram_id: int):
    """GEt user by telegram id."""
    return (
        db.query(models.User)
        .filter(models.User.telegram_id == user_telegram_id)
        .first()
    )


def get_articles_for_user(
    db: Session, user_telegram_id: int, skip: int = 0, limit: int = 100
):
    """Get user articles matching language code by user_telegram_id."""
    current_user = (
        db.query(models.User)
        .filter(models.User.telegram_id == user_telegram_id)
        .first()
    )
    return (
        db.query(models.Article)
        .order_by(models.Article.id)
        .filter(models.Article.language_code == current_user.language_code)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user(db: Session, user: schemas.UserCreate):
    """Create new user providing telegram id."""
    db_user = models.User(
        telegram_id=user.telegram_id,
        username=user.username,
        pet_name=user.pet_name,
        language_code=user.language_code,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def enable_user(db: Session, telegram_id: int, user: schemas.UserEnable):
    """Enable or disable user receiving messages providing telegram id."""
    db_user = (
        db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    )
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    """Get all users."""
    return (
        db.query(models.User)
        .filter(models.User.active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_all_articles(db: Session, skip: int = 0, limit: int = 100):
    """Get all articles."""
    return (
        db.query(models.Article)
        .order_by(models.Article.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_article(db: Session, article_id: int):
    """Get single article by id."""
    return db.query(models.Article).filter(models.Article.id == article_id).first()


def create_article(db: Session, article: schemas.ArticleCreate):
    """Create new article and save to DB."""
    db_article = models.Article(
        text=article.text,
        image_url=article.image_url,
        language_code=article.language_code,
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def set_article_sent(db: Session, data: schemas.SetSent):
    """Set article as sent for a user."""
    db_article = (
        db.query(models.Article).filter(models.Article.id == data.article_id).first()
    )
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with this id not found",
        )

    db_user = db.query(models.User).filter(models.User.id == data.user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with this id not found"
        )

    db_user.sent_articles.append(db_article)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
