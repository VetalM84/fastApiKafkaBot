"""POST endpoint for articles."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.database import get_db
import schemas
from db import crud

router = APIRouter(prefix='/articles', tags=["article"])


@router.post("/", response_model=schemas.ArticleCreate, status_code=status.HTTP_201_CREATED)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    """Create new article."""
    return crud.create_article(db=db, article=article)
