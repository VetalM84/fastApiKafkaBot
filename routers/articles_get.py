from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
import schemas
from db import crud

router = APIRouter(prefix='/articles', tags=["article"])


@router.get(
    "/{telegram_id}/user",
    response_model=list[schemas.ArticleBase],
    status_code=status.HTTP_200_OK,
)
def read_user_articles(telegram_id: int, db: Session = Depends(get_db)):
    """Get user articles matching language code and user_telegram_id."""
    db_articles = crud.get_articles_for_user(db, user_telegram_id=telegram_id)
    if db_articles is None:
        raise HTTPException(status_code=404, detail="Articles not found")
    return db_articles


@router.get("/", response_model=list[schemas.ArticleBase])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Read all articles."""
    items = crud.get_all_articles(db, skip=skip, limit=limit)
    return items


@router.get("/{article_id}/user_list")
def read_sent_list(article_id: int, db: Session = Depends(get_db)):
    """Read single article by id and return a list of user id article sent to."""
    db_article = crud.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    list_sent_to_user = [i.telegram_id for i in db_article.sent_to_user]
    print("list", list_sent_to_user)
    return list_sent_to_user


@router.get("/{article_id}", response_model=schemas.ArticleBase)
def read_article(article_id: int, db: Session = Depends(get_db)):
    """Read single article by id."""
    db_article = crud.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article
