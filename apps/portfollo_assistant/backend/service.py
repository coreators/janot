from sqlalchemy.orm import Session
from . import models, schemas


# user 관련은 user_service.py
# portfolio 관련은 portfolio_service.py
# trading_journal 관련은 trading_journal_service.py
# monthly_trade 관련은 monthly_trade_service.py
# daily_news 관련은 daily_news_service.py
# my_watchlist 관련은 my_watchlist_service.py
# ai_assistant 관련은 ai_assistant_service.py
# finance 정보 가져와서 계산하는거는 어디서해야할지?

# login 시, user 정보를 가져옴
# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()
#
# # sign in 시, user 정보를 전달
# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(username=user.username, email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
