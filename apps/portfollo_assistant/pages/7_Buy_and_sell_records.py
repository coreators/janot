import streamlit as st
from pydantic import BaseModel, Field
import streamlit_pydantic as sp
from streamlit_searchbox import st_searchbox
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from backend.schemas import KorBuyJournalModel, KorSellJournalModel
from pathlib import Path
import pandas as pd

usernameSession = 'username'
userSession = st.session_state[usernameSession]

st.markdown("# Buy, Sell Records")
st.sidebar.markdown("# Buy, Sell Records")

buy_or_sell = st.sidebar.selectbox("매수 매도 선택", ["매수", "매도"])

username = "sanghyeok"

total, korea, usa, dollar= st.tabs(['Total', 'Korea', 'USA',"Dollar"])
st.sidebar.success("Trading Journal ➕")
st.sidebar.info(" 매수 매도 기록 페이지입니다.")
st.sidebar.title("Trading Journal ➕")
st.sidebar.markdown(
    """
    매수 매도 기록 페이지입니다.
    """
)

# 미리 저장해둔 데이터 읽어오기
kor_list_name = pd.read_csv("resources/kor_ticker_list.csv")['Name']
kor_list_code = pd.read_csv("resources/kor_ticker_list.csv")['Code']

usa_list_name = pd.read_csv("resources/usa_ticker_list.csv")['Name']
usa_list_code = pd.read_csv("resources/usa_ticker_list.csv")['Code']



def sync_with_tickerbox():
    st.session_state.ticker = kor_list_code[kor_list_name == st.session_state.ticker_searchbox].values[0]

def send_buy_journal(ticker, buy_price, buy_amount, buy_date, tax, fee):
    # TODO : send buy journal to backend
    print("buy",ticker, buy_price, buy_amount, buy_date, tax, fee)
    pass

def send_sell_journal(ticker, sell_price, sell_amount, sell_date, tax, fee):
    # TODO : send sell journal to backend
    print("sell",ticker, sell_price, sell_amount, sell_date, tax, fee)
    pass

with total:
    st.empty()
    st.title("All Accounts")

with korea:
    # TODO : 매수매도 페이지 따로 만들어서 옮기기
    if buy_or_sell == "매수":
        st.empty()
        st.title("한국 주식 매수 일지 작성")
        # pandas나 numpy로 배열 바꿀 수 있음. box를 yahoo finance에서 가져온 data frame으로 바꾸기
        search_box = st.selectbox("회사 이름", kor_list_name, key="ticker_searchbox", on_change=sync_with_tickerbox)
        st.info("회사 이름을 입력하면 해당 티커를 아래 박스에 자동으로 채워줍니다.")
        # schemas.py : ticker price amount date tax fee
        ticker = st.text_input("티커",disabled=True, key="ticker", value=kor_list_code[0]) # 회사이름으로 ticker 검색해서 ticker 부분에 넣기
        buy_price = st.number_input("매수 가격", key="buy_price", min_value=0, value=0, step=100, format=None)
        buy_amount = st.number_input("매수 수량", key="buy_amount", min_value=0, value=0, step=1, format=None)
        buy_date = st.date_input("매수 일자", key="buy_date", value=None, min_value=None, max_value=None, help=None)
        tax = st.number_input("수수료율", key="tax", min_value=0.0, value=0.05, step=0.01, format=None, help="키움증권의 수수료율은 0.05% 입니다")
        fee = st.number_input("거래세율", key="fee", min_value=0.0, value=0.01, step=0.01, format=None, help="키움증권의 수수료율은 0.01% 입니다")
        submit = st.button("Submit")
        if submit:
            send_buy_journal(ticker, buy_price, buy_amount, buy_date, tax, fee)
            # add error handling
            # print warning whether data is correct or not
    else:
        st.empty()
        st.title("한국 주식 매도 일지 작성")
        search_box = st.selectbox("회사 이름", kor_list_name, key="ticker_searchbox", on_change=sync_with_tickerbox)
        st.info("회사 이름을 입력하면 해당 티커를 아래 박스에 자동으로 채워줍니다.")
        # schemas.py : ticker price amount date tax fee
        ticker = st.text_input("티커",disabled=True, key="ticker", value=kor_list_code[0]) # 회사이름으로 ticker 검색해서 ticker 부분에 넣기
        sell_price = st.number_input("매도 가격", key="buy_price", min_value=0, value=0, step=100, format=None)
        sell_amount = st.number_input("매도 수량", key="buy_amount", min_value=0, value=0, step=1, format=None)
        sell_date = st.date_input("매도 일자", key="buy_date", value=None, min_value=None, max_value=None, help=None)
        tax = st.number_input("수수료율", key="tax", min_value=0.0, value=0.05, step=0.01, format=None, help="키움증권의 수수료율은 0.05% 입니다")
        fee = st.number_input("거래세율", key="fee", min_value=0.0, value=0.01, step=0.01, format=None, help="키움증권의 수수료율은 0.01% 입니다")
        submit = st.button("Submit")
        if submit:
            send_sell_journal(ticker, sell_price, sell_amount, sell_date, tax, fee)
            # add error handling
            # print warning whether data is correct or not
with usa:
    st.empty()
