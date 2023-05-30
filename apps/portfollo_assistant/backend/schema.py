from pydantic import BaseModel

# user schema
# TODO : portfolio schema, trading_journal schema, monthly_trade schema, daily_news schema, my_watchlist schema, ai_assistant schema

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
