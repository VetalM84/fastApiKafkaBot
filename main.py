"""Main startup file for the FastAPI application with links to endpoints."""

from fastapi import FastAPI

from db import models
from db.database import engine
from routers import articles_get, articles_post, users_get, users_post

app = FastAPI()
app.include_router(articles_get.router)
app.include_router(articles_post.router)
app.include_router(users_get.router)
app.include_router(users_post.router)

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def index():
    """Check health server status."""
    return {"message": "Server is OK!"}
