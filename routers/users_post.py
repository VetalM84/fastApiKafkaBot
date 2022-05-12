from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
import schemas
from db import crud

router = APIRouter(prefix='/users', tags=["user"])


@router.post("/", response_model=schemas.UserBase, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create new user providing telegram id."""
    db_user = crud.get_user(db, user_telegram_id=user.telegram_id)
    if db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Telegram id is already registered")
    return crud.create_user(db=db, user=user)


# @app.post("/users/{user_id}/items/", response_model=schemas.Item, tags=["item"])
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
