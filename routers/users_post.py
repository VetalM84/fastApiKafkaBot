"""Post endpoints for users."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
import schemas
from db import crud

router = APIRouter(prefix="/users", tags=["user"])


@router.post("/", response_model=schemas.UserBase, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create new user providing telegram id."""
    db_user = crud.get_user(db, user_telegram_id=user.telegram_id)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Telegram id is already registered",
        )
    return crud.create_user(db=db, user=user)


@router.patch(
    "/{telegram_id}/enable",
    response_model=schemas.UserBase,
    status_code=status.HTTP_200_OK,
)
async def toggle_user_status(
    telegram_id: int, user: schemas.UserEnable, db: Session = Depends(get_db)
):
    """Enable or disable user receiving messages providing telegram id."""
    db_user = crud.get_user(db, user_telegram_id=telegram_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Telegram id is not registered",
        )
    return crud.enable_user(db=db, telegram_id=telegram_id, user=user)


@router.post("/set_sent", status_code=status.HTTP_201_CREATED)
async def set_article_sent(data: schemas.SetSent, db: Session = Depends(get_db)):
    """Set article as sent for a user."""
    return crud.set_article_sent(db=db, data=data)
