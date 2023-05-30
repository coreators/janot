from pydantic import BaseModel, Field
import datetime
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

class KorBuyJournalModel(BaseModel):
    ticker: str = Field(..., description="티커를 입력하세요") # 잘못된 티커에 대해서 처리를 해야함.
    price: int = Field(..., description="매수가격을 입력하세요")
    amount: int = Field(..., description="수량을 입력하세요")
    date: datetime.date = Field(..., description="매수/매도 일자를 지정해주세요")
    tax: float = Field(..., description="수수료율을 선택하세요") # 수수료율 설명을 추가하기
    fee: float = Field(..., description="거래세율을 선택하세요") # 거래세율 설명을 추가하기 얘는 넣을지 말지 고민해보기

class KorSellJournalModel(BaseModel):
    ticker: str = Field(..., description="티커를 입력하세요") # 잘못된 티커에 대해서 처리를 해야함.
    price: int = Field(..., description="매도 가격을 입력하세요")
    amount: int = Field(..., description="매도 수량을 입력하세요") # 가지고 있는것 이상으로 처리하지 못하게 하기
    date: datetime.date = Field(..., description="매도 일자를 지정해주세요")
    tax: float = Field(..., description="수수료율을 선택하세요") # 수수료율 설명을 추가하기
    fee: float = Field(..., description="거래세율을 선택하세요") # 거래세율 설명을 추가하기 얘는 넣을지 말지 고민해보기
