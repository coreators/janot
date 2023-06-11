from sqlalchemy import Column, Integer, String, DateTime ,Boolean, ForeignKey,Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Must be same as postgresql table name and contents

class User(Base):
    __tablename__ = "portfoliouser"
    userid = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    passwordhash = Column(String)
    relationship("kor_daily_journal")
    relationship("usa_daily_journal")

class KorDailyJournal(Base):
    __tablename__ = "kor_daily_journal"
    transaction_id = Column(Integer, primary_key=True, index=True) # id는 자동으로 생성되는 것으로 하기
    email = Column(String, ForeignKey("portfoliouser.email")) # user_id는 자동으로 생성되는 것으로 하기
    ticker = Column(String)   # ticker는 유니크한 값으로 하기
    price = Column(Integer)                            # price per share
    amount = Column(Integer)
    date = Column(DateTime)
    tax = Column(Integer)
    fee = Column(Integer)
    is_buy = Column(Boolean) # 매수인지 매도인지 구분하는 변수
    sector = Column(String) # 주식이 어디 산업에 해당하는지 기록, 저장 하는게 편하긴할듯.
    sold_amount = Column(Integer)
    profit_loss = Column(Integer)

class UsaDailyJournal(Base):
    __tablename__ = "usa_daily_journal"
    transaction_id = Column(Integer, primary_key=True, index=True) # id는 자동으로 생성되는 것으로 하기
    email = Column(String, ForeignKey("portfoliouser.email")) # user_id는 자동으로 생성되는 것으로 하기
    ticker = Column(String)   # ticker는 유니크한 값으로 하기
    price = Column(Numeric)   # price per share
    amount = Column(Integer)
    date = Column(DateTime)
    tax = Column(Integer)
    fee = Column(Integer)
    exchange_rate = Column(Numeric)
    is_buy = Column(Boolean) # 매수인지 매도인지 구분하는 변수
    sector = Column(String) # 주식이 어디 산업에 해당하는지 기록, 저장 하는게 편하긴할듯.
    sold_amount = Column(Integer)
    profit_loss = Column(Numeric) # in dollars
    profit_loss_with_exchange = Column(Numeric) # in won

