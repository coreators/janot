import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from models import User, KorDailyJournal
from database import SessionLocal, engine, get_db
from schemas import UserCreate ,UserLogin


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


# front에서 보낸 데이터를 받아서 처리하는 방법은 어떻게 하는지 알아보기

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=9000)