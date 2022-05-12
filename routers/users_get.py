from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
import schemas
from db import crud

router = APIRouter(prefix='/users', tags=["user"])


@router.get("/{telegram_id}", response_model=schemas.UserBase, status_code=status.HTTP_200_OK)
def read_user(telegram_id: int, db: Session = Depends(get_db)):
    """Read user by telegram id without list of sent articles."""
    db_user = crud.get_user(db, user_telegram_id=telegram_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.get(
    "/{telegram_id}/articles",
    response_model=schemas.UserArticlesSentView
)
def read_user_with_sent_articles(telegram_id: int, db: Session = Depends(get_db)):
    """Get user info with a list of sent articles matching language code and user_telegram_id."""
    db_articles = crud.get_user(db, user_telegram_id=telegram_id)
    if db_articles is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_articles
