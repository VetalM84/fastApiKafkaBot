from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """DB Session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/users/", response_model=list[schemas.User], tags=["user"])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


@app.post("/users/", response_model=schemas.UserBase, tags=["user"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create new user providing telegram id."""
    db_user = crud.get_user(db, user_telegram_id=user.telegram_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Telegram id is already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_telegram_id}", response_model=schemas.UserBase, tags=["user"])
def read_user(user_telegram_id: int, db: Session = Depends(get_db)):
    """Read user by telegram id."""
    db_user = crud.get_user(db, user_telegram_id=user_telegram_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get(
    "/articles/{user_telegram_id}",
    response_model=list[schemas.ArticleBase],
    tags=["article"],
)
def read_user_articles(user_telegram_id: int, db: Session = Depends(get_db)):
    db_articles = crud.get_user_articles(db, user_telegram_id=user_telegram_id)
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    return db_articles


# @app.post("/users/{user_id}/items/", response_model=schemas.Item, tags=["item"])
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.post("/articles/", response_model=schemas.ArticleCreate, tags=["article"])
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    """Create new article."""
    return crud.create_article(db=db, article=article)


@app.get("/articles/", response_model=list[schemas.ArticleBase], tags=["article"])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Read all articles."""
    items = crud.get_articles(db, skip=skip, limit=limit)
    return items


@app.get("/articles/{article_id}", response_model=schemas.ArticleBase, tags=["article"])
def read_article(article_id: int, db: Session = Depends(get_db)):
    """Read article by id."""
    db_article = crud.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article
