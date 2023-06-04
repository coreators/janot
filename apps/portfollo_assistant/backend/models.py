from sqlalchemy import Column, Integer, String, Date ,Boolean, ForeignKey
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

class KorDailyJournal(Base):
    __tablename__ = "kor_daily_journal"
    transaction_id = Column(Integer, primary_key=True, index=True) # id는 자동으로 생성되는 것으로 하기
    user_id = Column(Integer, ForeignKey("users.id")) # user_id는 자동으로 생성되는 것으로 하기
    ticker = Column(String, unique=True, index=True)   # ticker는 유니크한 값으로 하기
    price = Column(Integer)                            # price per share
    amount = Column(Integer)
    date = Column(Date)
    tax = Column(Integer)
    fee = Column(Integer)
    is_buy = Column(Boolean) # 매수인지 매도인지 구분하는 변수
    #classification = Column(String) # 주식이 어디 산업에 해당하는지 기록, 저장 하는게 편하긴할듯.

# 미국주식용 클래스 작성하기

