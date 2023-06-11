import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from models import User, KorDailyJournal, UsaDailyJournal
from database import SessionLocal, engine, get_db
from schemas import UserCreate ,UserLogin, KorJournalCreate,KorJournalUpdate,\
    UsaJournalCreate, KorJournalReadRequest, KorJournalRead, KorJournalBuyRecords, \
    UsaJournalRead, UsaJournalReadRequest, UsaJournalReadBuyRecords, UsaJournalUpdate
from typing import List


from passlib.context import CryptContext

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# 데이터베이스에 연결


# 여기서 세션 연결해두고 요청이 오면 연결해서 전달해야할것으로 보임.


app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

#일단 여기에 request 관련 코드 다 짜고 service.py로 분리하던지 하기

@app.on_event("startup")
async def startup_event():
    #여기서 create_ticker_list 함수를 실행시켜서 ticker_list를 만들어 줘야할수도 있음.
    # do something when the server starts up
    pass


@app.on_event("shutdown")
async def shutdown_event():
    # do something when the server shuts down

    pass
@app.get("/")
async def homepage(request: Request):
    return {"message": "Hello World"}

# TODO : change post and db format
# following is for testing


@app.post("/register")
async def create_user(user: UserCreate,db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, passwordhash=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": f"User {user.username} registered successfully"}

@app.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):       # Userlogin은 schemas.py에 정의되어있음, Pydantic 클래스임
    db_user = db.query(User).filter(User.email == user.email).first()       # query 안엔 sqlalchemy의 모델을 넣어야함.
    if not db_user:
        return {"message": "Invalid Credentials"}
    if not verify_password(user.password, bytes(db_user.passwordhash)):
        return {"message": "Incorrect password"}
    return {"message": "Logged in successfully"}

@app.post("/api/v1/journal/kor/trade")
async def add_kor_journal(korJournal: KorJournalCreate, db: Session = Depends(get_db)):
    new_kor_buy_journal = KorDailyJournal(
        email=korJournal.email,
        ticker=korJournal.ticker,
        price=korJournal.price,
        amount=korJournal.amount,
        date=korJournal.date,
        tax=korJournal.tax,
        fee=korJournal.fee,
        is_buy=korJournal.is_buy,
        sector=korJournal.sector,
        sold_amount=korJournal.sold_amount,
        profit_loss=korJournal.profit_loss)
    db.add(new_kor_buy_journal)
    db.commit()
    return {"message": "Kor buy journal added successfully"}

@app.post("/api/v1/journal/usa/trade")
async def add_usa_journal(usaJournal: UsaJournalCreate, db: Session = Depends(get_db)):
    new_usa_buy_journal = UsaDailyJournal(
        email=usaJournal.email,
        ticker=usaJournal.ticker,
        price=usaJournal.price,
        amount=usaJournal.amount,
        date=usaJournal.date,
        tax=usaJournal.tax,
        fee=usaJournal.fee,
        exchange_rate=usaJournal.exchange_rate,
        is_buy=usaJournal.is_buy,
        sector=usaJournal.sector,
        sold_amount=usaJournal.sold_amount,
        profit_loss=usaJournal.profit_loss,
        profit_loss_with_exchange=usaJournal.profit_loss_with_exchange)
    db.add(new_usa_buy_journal)
    db.commit()
    return {"message": "Usa buy journal added successfully"}

@app.get("/api/v1/journal/kor/read", response_model=List[KorJournalRead]) #KorJournalRead는 schemas.py에 정의되어있음, Pydantic 클래스임
async def read_kor_journal(korJournalReadRequest: KorJournalReadRequest, db: Session = Depends(get_db)):
    kor_journal_db = db.query(KorDailyJournal).filter(KorDailyJournal.email == korJournalReadRequest.email).all() # query 안엔 sqlalchemy의 모델을 넣어야함.
    kor_journal = [KorJournalRead(**{k: v for k, v in item.__dict__.items() if not k.startswith('_')}) for item in kor_journal_db] # 받아온걸 pydantic 클래스로 변환
    return kor_journal

@app.get("/api/v1/journal/kor/buy/record", response_model=List[KorJournalRead])
async def read_kor_check_amount(korJournalBuyRecords: KorJournalBuyRecords, db: Session = Depends(get_db)):
    kor_journal_db = db.query(KorDailyJournal)\
        .filter(KorDailyJournal.email == korJournalBuyRecords.email)\
        .filter(KorDailyJournal.ticker == korJournalBuyRecords.ticker)\
        .filter(KorDailyJournal.is_buy == True).all()
    kor_journal = [KorJournalRead(**{k: v for k, v in item.__dict__.items() if not k.startswith('_')}) for item in kor_journal_db] # 받아온걸 pydantic 클래스로 변환
    return kor_journal

@app.put("/api/v1/journal/kor/buy/update")
async def update_kor_buy_record(korJournal: List[KorJournalUpdate], db: Session = Depends(get_db)):
    try:
        db.bulk_update_mappings(KorDailyJournal, korJournal)
        db.commit()
    except:
        db.rollback()
    return {"message": "Kor buy journal updated successfully"}

@app.get("/api/v1/journal/usa/read", response_model=List[UsaJournalRead]) #KorJournalRead는 schemas.py에 정의되어있음, Pydantic 클래스임
async def read_usa_journal(usaJournalReadRequest: UsaJournalReadRequest, db: Session = Depends(get_db)):
    usa_journal_db = db.query(UsaDailyJournal).filter(UsaDailyJournal.email == usaJournalReadRequest.email).all()
    usa_journal = [UsaJournalRead(**{k: v for k, v in item.__dict__.items() if not k.startswith('_')}) for item in usa_journal_db] # 받아온걸 pydantic 클래스로 변환
    return usa_journal

@app.get("/api/v1/journal/usa/buy/record", response_model=List[UsaJournalRead])
async def read_usa_check_amount(usaJournalReadBuyRecords: UsaJournalReadBuyRecords, db: Session = Depends(get_db)):
    usa_journal_db = db.query(UsaDailyJournal) \
        .filter(UsaDailyJournal.email == usaJournalReadBuyRecords.email) \
        .filter(UsaDailyJournal.ticker == usaJournalReadBuyRecords.ticker) \
        .filter(UsaDailyJournal.is_buy == True).all()
    usa_journal = [UsaJournalRead(**{k: v for k, v in item.__dict__.items() if not k.startswith('_')}) for item in usa_journal_db] # 받아온걸 pydantic 클래스로 변환
    return usa_journal

@app.put("/api/v1/journal/usa/buy/update")
async def update_kor_buy_record(usaJournal: List[UsaJournalUpdate], db: Session = Depends(get_db)):
    try:
        db.bulk_update_mappings(UsaDailyJournal, usaJournal)
        db.commit()
    except:
        db.rollback()
    return {"message": "Kor buy journal updated successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=9000)