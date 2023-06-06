import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from models import User, KorDailyJournal, UsaDailyJournal
from database import SessionLocal, engine, get_db
from schemas import UserCreate ,UserLogin, KorJournalCreate, UsaJournalCreate



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
        sector=korJournal.sector)
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
        sector=usaJournal.sector)
    db.add(new_usa_buy_journal)
    db.commit()
    return {"message": "Usa buy journal added successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=9000)