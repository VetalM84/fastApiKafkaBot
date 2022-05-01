from pydantic import BaseModel, HttpUrl, Field


class ArticleBase(BaseModel):
    text: str = Field(..., min_length=50, max_length=1024)
    image_url: HttpUrl = Field(..., title="Image URL")
    language_code: str = Field(..., max_length=3, min_length=2)

    class Config:
        orm_mode = True


class ArticleCreate(ArticleBase):
    pass


class ArticleEdit(ArticleBase):
    id: int


class UserBase(BaseModel):
    telegram_id: int = Field(..., ge=0)
    username: str = Field(..., max_length=50)
    pet_name: str = Field(..., max_length=50)
    language_code: str = Field(..., max_length=3, min_length=2)

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserEdit(UserBase):
    id: int
