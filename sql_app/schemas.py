from pydantic import BaseModel, HttpUrl, Field


class ArticleBase(BaseModel):
    """Base serializer for an article."""
    text: str = Field(..., min_length=50, max_length=1024)
    image_url: HttpUrl = Field(..., title="Image URL")
    language_code: str = Field('ru', max_length=3, min_length=2)

    class Config:
        """Enable ORM mode for all child methods."""
        orm_mode = True


class ArticleCreate(ArticleBase):
    """Serializer for creating an article."""
    pass


class ArticleEdit(ArticleBase):
    """Serializer for editing an article."""
    id: int


class UserBase(BaseModel):
    """Base serializer for a user."""
    telegram_id: int = Field(..., ge=0)
    username: str = Field(..., max_length=50)
    pet_name: str = Field(..., max_length=50)
    language_code: str = Field(..., max_length=3, min_length=2)

    class Config:
        """Enable ORM mode for all child methods."""
        orm_mode = True


class UserCreate(UserBase):
    """Serializer for creating a user."""
    pass


class UserEdit(UserBase):
    """Serializer for editing a user."""
    id: int
