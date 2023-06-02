import streamlit as st
from pydantic import BaseModel, Field
import streamlit_pydantic as sp
from streamlit_searchbox import st_searchbox
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from backend.schema import KorBuyJournalModel, KorSellJournalModel

# "st.session_state object:" , st.session_state

st.markdown("# Trading Journal")
st.sidebar.markdown("# Trading Journal")


total, korea, usa, dollar= st.tabs(['Total', 'Korea', 'USA',"Dollar"])
st.sidebar.success("Trading Journal 📝")
st.sidebar.info("여기는 매매일지 정리 페이지입니다.")
st.sidebar.title("Trading Journal 📝")
st.sidebar.markdown(
    """
    아래는 본 페이지의 요구사항 정리입니다.
    
    - 여기는 매매일지 페이지입니다.
    - 매매일지를 추가하고 삭제할 수 있습니다.
    - 내 엑셀 기능은 그대로 가져오기
    
    ## 매매일지 기본 기능
    - 직접 포트폴리오를 바꾸진 않게 ( 매수일자/매도일자로 구분)
    - 매수 일자 및 기업을 명시할 수 있어야함.
    - 세금을 기록할 수 있어야함. (왠만하면 알아서 되게)
    - 증권사별로 대표 세금 설정 가능해야 ( 수동으로도 바꿀 수 있어야함.)
    - 매수 매도 차액 반영 방식은 주로 사용하는 방식으로 하도록하기.
    - 검색기능
    
    ## 달러관련
    - 달러를 얼마에 샀는지?
    - 모른다면 그날 종가 기준 환율로
    - 미국자산을 얼마에샀는지
    - 환전 가격 기준으로 내가 얼마나 이득을 보고있는지
    
    """
)

buy_or_sell = st.sidebar.selectbox("매수 매도 선택", ["매수", "매도"])

def sync_with_tickerbox():
    # TODO : sync with search value
    st.session_state.ticker = "hello"

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
    st.title("Korea Accounts")
    # 아래 내용을 매수 일지 추가하는 탭에다가 넣든지 옮기기
    if buy_or_sell == "매수":
        st.empty()
        st.title("한국 주식 매수 일지 작성")
        st.text("티커를 입력하세요")
        # pandas나 numpy로 배열 바꿀 수 있음. box를 yahoo finance에서 가져온 data frame으로 바꾸기
        search_box = st.selectbox("회사 이름", ["hello", "world"], key="ticker_searchbox", on_change=sync_with_tickerbox)
        st.info("회사 이름을 입력하면 해당 티커를 아래 박스에 자동으로 채워줍니다.")
        # schema.py : ticker price amount date tax fee
        ticker = st.text_input("티커",disabled=True, key="ticker", value="ticker") # 회사이름으로 ticker 검색해서 ticker 부분에 넣기
        buy_price = st.number_input("매수 가격", key="buy_price", min_value=0, value=0, step=100, format=None)
        buy_amount = st.number_input("매수 수량", key="buy_amount", min_value=0, value=0, step=1, format=None)
        buy_date = st.date_input("매수 일자", key="buy_date", value=None, min_value=None, max_value=None, help=None)
        tax = st.number_input("수수료율", key="tax", min_value=0.0, value=0.05, step=0.01, format=None, help="키움증권의 수수료율은 0.05% 입니다")
        fee = st.number_input("거래세율", key="fee", min_value=0.0, value=0.01, step=0.01, format=None, help="키움증권의 수수료율은 0.01% 입니다")
        submit = st.button("Submit")
        if submit:
            send_buy_journal(ticker, buy_price, buy_amount, buy_date, tax, fee)
            # add error handling
    else:
        st.empty()
        st.title("한국 주식 매도 일지 작성")
        st.text("티커를 입력하세요")
        # pandas나 numpy로 배열 바꿀 수 있음. box를 yahoo finance에서 가져온 data frame으로 바꾸기
        search_box = st.selectbox("회사 이름", ["hello", "world"], key="ticker_searchbox", on_change=sync_with_tickerbox)
        st.info("회사 이름을 입력하면 해당 티커를 아래 박스에 자동으로 채워줍니다.")
        # schema.py : ticker price amount date tax fee
        ticker = st.text_input("티커",disabled=True, key="ticker", value="ticker") # 회사이름으로 ticker 검색해서 ticker 부분에 넣기
        sell_price = st.number_input("매도 가격", key="buy_price", min_value=0, value=0, step=100, format=None)
        sell_amount = st.number_input("매도 수량", key="buy_amount", min_value=0, value=0, step=1, format=None)
        sell_date = st.date_input("매도 일자", key="buy_date", value=None, min_value=None, max_value=None, help=None)
        tax = st.number_input("수수료율", key="tax", min_value=0.0, value=0.05, step=0.01, format=None, help="키움증권의 수수료율은 0.05% 입니다")
        fee = st.number_input("거래세율", key="fee", min_value=0.0, value=0.01, step=0.01, format=None, help="키움증권의 수수료율은 0.01% 입니다")
        submit = st.button("Submit")
        if submit:
            send_sell_journal(ticker, sell_price, sell_amount, sell_date, tax, fee)
            # add error handling

with usa:
    st.empty()
    st.title("USA Accounts")