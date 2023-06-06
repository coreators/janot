from pydantic import BaseModel, Field
import datetime
# user schema
# TODO : portfolio schema, trading_journal schema, monthly_trade schema, daily_news schema, my_watchlist schema, ai_assistant schema


# Including pydantic field type
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    username: str
    password: str

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


# models와 동일한지 확인하기

class KorJournalCreate(BaseModel):
    email: str                         # user_id는 자동으로 생성되는 것으로 하기
    ticker: str                        # ticker는 유니크한 값으로 하기
    price: int                         # price per share (원화로)
    amount: int
    date: datetime.date
    tax: int
    fee: int
    is_buy: bool # 매수인지 매도인지 구분하는 변수
    sector: str # 주식이 어디 산업에 해당하는지 기록, 저장 하는게 편하긴할듯.

class UsaJournalCreate(BaseModel):
    email: str
    ticker: str
    price: float
    amount: int
    date: datetime.date
    tax: int
    fee: int
    exchange_rate: float
    is_buy: bool # 매수인지 매도인지 구분하는 변수
    sector: str # 주식이 어디 산업에 해당하는지 기록, 저장 하는게 편하긴할듯.



# email과, is_buy를 제외하고 가져오기
# is_buy 여부는 request에서 처리해주기
class KorJournalRead(BaseModel):
    ticker: str
    price: int
    amount: int
    date: datetime.date
    tax: int
    fee: int
    sector: str # 주식이 어디 산업에 해당하는지 기록, 저장 하는게 편하긴할듯.
    is_buy: bool

class KorJournalReadRequest(BaseModel):
    email: str