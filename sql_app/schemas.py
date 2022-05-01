from pydantic import BaseModel, HttpUrl


class ArticleBase(BaseModel):
    text: str
    image_url: str
    language_code: str

    class Config:
        orm_mode = True


class ArticleCreate(ArticleBase):
    pass


class ArticleEdit(ArticleBase):
    id: int


class UserBase(BaseModel):
    telegram_id: int
    username: str
    pet_name: str
    language_code: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserEdit(UserBase):
    id: int
