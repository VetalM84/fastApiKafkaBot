"""Functions to create, read, update, and delete data from the database."""

from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_telegram_id: int):
    """GEt user by telegram id."""
    return (
        db.query(models.User)
        .filter(models.User.telegram_id == user_telegram_id)
        .first()
    )


def get_sent_to_user_articles(db: Session, user_telegram_id: int):
    """Get user articles matching language code and user_telegram_id."""
    return (
        db.query(models.User)
        .filter(models.User.telegram_id == user_telegram_id)
        .first()
    )


def get_user_articles(
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
        .filter(models.Article.language_code == current_user.language_code)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user(db: Session, user: schemas.UserCreate):
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


def get_all_articles(db: Session, skip: int = 0, limit: int = 100):
    """Get all articles."""
    return db.query(models.Article).offset(skip).limit(limit).all()


def get_article(db: Session, article_id: int):
    """Get single article by id."""
    return db.query(models.Article).filter(models.Article.id == article_id).first()


def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.Article(
        text=article.text,
        image_url=article.image_url,
        language_code=article.language_code,
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article
