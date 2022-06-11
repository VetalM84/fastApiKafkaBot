"""Schemas for request body data validation. Works both for input and output."""

from typing import List

from pydantic import BaseModel, HttpUrl, Field


class UserInArticleView(BaseModel):
    """What fields will be in nested sent_to_user list."""

    # id: int
    telegram_id: int

    class Config:
        """Enable ORM mode."""

        orm_mode = True


class ArticleBase(BaseModel):
    """Base serializer for an article."""

    id: int
    text: str = Field(..., min_length=50, max_length=1024)
    image_url: HttpUrl = Field(..., title="Image URL")
    language_code: str = Field("ru", max_length=3, min_length=2)
    sent_to_user: List[UserInArticleView] = []

    class Config:
        """Enable ORM mode for all child methods."""

        orm_mode = True


class ArticleResponse(ArticleBase):
    sent_to_user: List[int] = []


class ArticleCreate(BaseModel):
    """Serializer for creating an article."""

    text: str = Field(..., min_length=50, max_length=1024)
    image_url: HttpUrl = Field(..., title="Image URL")
    language_code: str = Field("ru", max_length=3, min_length=2)

    class Config:
        """Enable ORM mode for all child methods."""

        orm_mode = True


class ArticleSentView(BaseModel):
    """What fields will be in nested sent_articles list."""

    id: int

    class Config:
        """Enable ORM mode."""

        orm_mode = True


class UserBase(BaseModel):
    """Base serializer for a user."""

    telegram_id: int = Field(..., ge=0)
    username: str = Field(..., max_length=50)
    pet_name: str = Field(..., max_length=50)
    language_code: str = Field(..., max_length=3, min_length=2)

    # sent_articles: List[ArticleBase] = []

    class Config:
        """Enable ORM mode for all child methods."""

        orm_mode = True


class UserInfo(BaseModel):
    """Get all users ids."""

    id: int
    telegram_id: int
    language_code: str

    class Config:
        """Enable ORM mode for all child methods."""

        orm_mode = True


class UserArticlesSentView(UserBase):
    """What fields will be in nested sent_articles list."""

    sent_articles: List[ArticleSentView] = []

    class Config:
        """Enable ORM mode."""

        orm_mode = True


class UserCreate(UserBase):
    """Serializer for creating a user."""

    pass


class UserEdit(UserBase):
    """Serializer for editing a user."""

    id: int


class SetSent(BaseModel):
    """Set article as sent for user."""

    user_id: int = Field(..., ge=0)
    article_id: int = Field(..., ge=0)

    class Config:
        """Enable ORM mode."""

        orm_mode = True
