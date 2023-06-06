import datetime

import streamlit as st
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pandas as pd
import requests

usernameSession = 'username'
userSession = st.session_state[usernameSession]

st.markdown("# Buy, Sell Records")
st.sidebar.markdown("# Buy, Sell Records")

buy_or_sell = st.sidebar.selectbox("매수 매도 선택", ["매수", "매도"])

username = "sanghyeok"

korea, usa, dollar= st.tabs(['Korea', 'USA',"Dollar"])
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
kor_list_sector = pd.read_csv("resources/kor_ticker_list.csv")['Sector']

usa_list_name = pd.read_csv("resources/usa_ticker_list.csv")['Name']
usa_list_code = pd.read_csv("resources/usa_ticker_list.csv")['Code']
usa_list_sector = pd.read_csv("resources/usa_ticker_list.csv")['Sector']


def kor_sync_with_ticker_and_sector():
    st.session_state.ticker = kor_list_code[kor_list_name == st.session_state.ticker_searchbox].values[0]
    st.session_state.sector = kor_list_sector[kor_list_name == st.session_state.ticker_searchbox].values[0]

def usa_sync_with_ticker_and_sector():
    st.session_state.usa_ticker = usa_list_code[usa_list_name == st.session_state.usa_ticker_searchbox].values[0]
    st.session_state.usa_sector = usa_list_sector[usa_list_name == st.session_state.usa_ticker_searchbox].values[0]



def send_buy_journal(ticker, buy_price, buy_amount, buy_date, tax, fee, sector):
    print("buy ",ticker, buy_price, buy_amount, buy_date, tax, fee)
    response = requests.post('http://localhost:9000/api/v1/journal/kor/trade',
                             json={'email':st.session_state[usernameSession],
                                 'ticker': ticker, 'price': buy_price, 'amount': buy_amount, 'date': buy_date.isoformat(), 'tax': tax, 'fee': fee,
                                   'is_buy': True, 'sector': sector})
    return response


def send_sell_journal(ticker, sell_price, sell_amount, sell_date, tax, fee, sector):
    print("sell",ticker, sell_price, sell_amount, sell_date, tax, fee)
    # TODO : 이전 매수기록에 충분한 보유량이 남아있는지 체크도 해주면 좋을듯.
    response = requests.post('http://localhost:9000/api/v1/journal/kor/trade',
                             json={'email':st.session_state[usernameSession],
                                   'ticker': ticker, 'price': sell_price, 'amount': sell_amount, 'date': sell_date.isoformat(), 'tax': tax, 'fee': fee,
                                   'is_buy': False, 'sector': sector})
    return response

def usa_send_buy_journal(ticker, buy_price, buy_amount, buy_date, tax, fee, sector, exchange_rate):
    print("buy ",ticker, buy_price, buy_amount, buy_date, tax, fee)
    response = requests.post('http://localhost:9000/api/v1/journal/usa/trade',
                             json={'email':st.session_state[usernameSession],
                                 'ticker': ticker, 'price': buy_price, 'amount': buy_amount, 'date': buy_date.isoformat(), 'tax': tax, 'fee': fee,
                                   'is_buy': True, 'sector': sector, 'exchange_rate':exchange_rate})
    return response

def usa_send_sell_journal(ticker, sell_price, sell_amount, sell_date, tax, fee, sector ,exchange_rate):
    print("sell",ticker, sell_price, sell_amount, sell_date, tax, fee)
    # TODO : 이전 매수기록에 충분한 보유량이 남아있는지 체크도 해주면 좋을듯.
    response = requests.post('http://localhost:9000/api/v1/journal/usa/trade',
                             json={'email':st.session_state[usernameSession],
                                   'ticker': ticker, 'price': sell_price, 'amount': sell_amount, 'date': sell_date.isoformat(), 'tax': tax, 'fee': fee,
                                   'is_buy': False, 'sector': sector, 'exchange_rate':exchange_rate})
    return response


# 한국 주식 기록 탭
with korea:
    if buy_or_sell == "매수":
        st.empty()
        st.title("한국 주식 매수 일지 작성")
        # pandas나 numpy로 배열 바꿀 수 있음. box를 yahoo finance에서 가져온 data frame으로 바꾸기
        search_box = st.selectbox("회사 이름", kor_list_name, key="ticker_searchbox", on_change=kor_sync_with_ticker_and_sector)
        st.info("회사 이름을 선택하면 회사 코드와 섹터가 자동으로 채워집니다.")
        # schemas.py : ticker price amount date tax fee
        ticker = st.text_input("티커",disabled=True, key="ticker", value=kor_list_code[0])
        sector = st.text_input("섹터", disabled=True, key="sector", value=kor_list_sector[0])
        buy_price = st.number_input("매수 가격", key="buy_price", min_value=0, value=0, step=100, format=None)
        buy_amount = st.number_input("매수 수량", key="buy_amount", min_value=1, value=1, step=1, format=None)
        buy_date = st.date_input("매수 일자", key="buy_date", value=None, min_value=None, max_value=datetime.date.today(), help=None)
        tax = st.number_input("수수료율", key="tax", min_value=0.0, value=0.05, step=0.01, format=None, help="키움증권의 수수료율은 0.05% 입니다")
        fee = st.number_input("거래세율", key="fee", min_value=0.0, value=0.01, step=0.01, format=None, help="키움증권의 수수료율은 0.01% 입니다")
        submit = st.button(label="Submit",key="kor_buy_submit")
        if submit:
            response = send_buy_journal(ticker, buy_price, buy_amount, buy_date, tax, fee, sector)
            print(buy_date)
            if response.status_code == 200:
                st.success("매수 기록 등록이 완료했습니다!")
                request_summary = search_box + "에 대한 매수 기록이 등록되었습니다."
                st.info(request_summary) #좀 더 구체적으로 쓰기
            else:
                st.error("매수 기록 등록이 실패했습니다!")
                st.stop()
            # add error handling
            # print warning whether data is correct or not
    else:
        st.empty()
        st.title("한국 주식 매도 일지 작성")
        search_box = st.selectbox("회사 이름", kor_list_name, key="ticker_searchbox", on_change=kor_sync_with_ticker_and_sector)
        st.info("회사 이름을 선택하면 회사 코드와 섹터가 자동으로 채워집니다.")
        # schemas.py : ticker price amount date tax fee
        ticker = st.text_input("티커", disabled=True, key="ticker", value=kor_list_code[0]) # 회사이름으로 ticker 검색해서 ticker 부분에 넣기
        sector = st.text_input("섹터", disabled=True, key="sector", value=kor_list_sector[0])
        sell_price = st.number_input("매도 가격", key="buy_price", min_value=0, value=0, step=100, format=None)
        sell_amount = st.number_input("매도 수량", key="buy_amount", min_value=0, value=0, step=1, format=None)
        sell_date = st.date_input("매도 일자", key="buy_date", value=None, min_value=None, max_value=datetime.date.today(), help=None)
        tax = st.number_input("수수료율", key="tax", min_value=0.0, value=0.05, step=0.01, format=None, help="키움증권의 수수료율은 0.05% 입니다")
        fee = st.number_input("거래세율", key="fee", min_value=0.0, value=0.01, step=0.01, format=None, help="키움증권의 수수료율은 0.01% 입니다")
        submit = st.button(label="Submit",key="kor_sell_submit")
        if submit:
            response = send_sell_journal(ticker, sell_price, sell_amount, sell_date, tax, fee, sector)
            if response.status_code == 200:
                st.success("매도 기록 등록이 완료했습니다!")
                request_summary = search_box + "에 대한 매도 기록이 등록되었습니다."
                st.info(request_summary)
            else:
                st.error("매도 기록 등록이 실패했습니다!")
                st.stop()

# 미국 주식 기록 탭
with usa:
    if buy_or_sell == "매수":
        st.empty()
        st.title("미국 주식 매수 일지 작성")
        # pandas나 numpy로 배열 바꿀 수 있음. box를 yahoo finance에서 가져온 data frame으로 바꾸기
        search_box = st.selectbox("회사 이름", usa_list_name, key="usa_ticker_searchbox", on_change=usa_sync_with_ticker_and_sector)
        st.info("회사 이름을 선택하면 회사 코드와 섹터가 자동으로 채워집니다.")
        # schemas.py : ticker price amount date tax fee
        ticker = st.text_input("티커", disabled=True, key="usa_ticker", value=usa_list_code[0])
        sector = st.text_input("섹터", disabled=True, key="usa_sector", value=usa_list_sector[0])
        buy_price = st.number_input("매수 가격", key="usa_buy_price", min_value=0.0, value=0.0, step=0.01, format=None)
        buy_amount = st.number_input("매수 수량", key="usa_buy_amount", min_value=1, value=1, step=1, format=None)
        buy_date = st.date_input("매수 일자", key="usa_buy_date", value=None, min_value=None, max_value=datetime.date.today(), help=None)
        tax = st.number_input("수수료율", key="usa_tax", min_value=0.0, value=0.05, step=0.01, format=None, help="키움증권의 수수료율은 0.05% 입니다")
        fee = st.number_input("거래세율", key="usa_fee", min_value=0.0, value=0.01, step=0.01, format=None, help="키움증권의 수수료율은 0.01% 입니다")
        exchange_rate = st.number_input("환율", key="exchange_rate", min_value=0.0, value=1300.00, step=0.01, format=None, help="달러당 원화 환율을 입력해주세요")
        submit = st.button(label="Submit",key="usa_buy_submit")
        if submit:
            response = usa_send_buy_journal(ticker, buy_price, buy_amount, buy_date, tax, fee, sector,exchange_rate)
            print(buy_date)
            if response.status_code == 200:
                st.success("매수 기록 등록이 완료했습니다!")
                request_summary = search_box + "에 대한 매수 기록이 등록되었습니다."
                st.info(request_summary) #좀 더 구체적으로 쓰기
            else:
                st.error("매수 기록 등록이 실패했습니다!")
                st.stop()
            # add error handling
            # print warning whether data is correct or not
    else:
        st.empty()
        st.title("미국 주식 매도 일지 작성")
        search_box = st.selectbox("회사 이름", usa_list_name, key="usa_ticker_searchbox", on_change=usa_sync_with_ticker_and_sector)
        st.info("회사 이름을 선택하면 회사 코드와 섹터가 자동으로 채워집니다.")
        # schemas.py : ticker price amount date tax fee
        ticker = st.text_input("티커",disabled=True, key="usa_ticker", value=usa_list_code[0])
        sector = st.text_input("섹터", disabled=True, key="usa_sector", value=usa_list_sector[0])
        buy_price = st.number_input("매도 가격", key="usa_buy_price", min_value=0.0, value=0.0, step=0.01, format=None)
        buy_amount = st.number_input("매도 수량", key="usa_buy_amount", min_value=1, value=1, step=1, format=None)
        buy_date = st.date_input("매도 일자", key="usa_buy_date", value=None, min_value=None, max_value=datetime.date.today(), help=None)
        tax = st.number_input("수수료율", key="usa_tax", min_value=0.0, value=0.05, step=0.01, format=None, help="키움증권의 수수료율은 0.05% 입니다")
        fee = st.number_input("거래세율", key="usa_fee", min_value=0.0, value=0.01, step=0.01, format=None, help="키움증권의 수수료율은 0.01% 입니다")
        exchange_rate = st.number_input("환율", key="exchange_rate", min_value=0.0, value=1300.00, step=0.01, format=None, help="달러당 원화 환율을 입력해주세요")
        submit = st.button(label="Submit",key="usa_sell_submit")
        if submit:
            response = usa_send_sell_journal(ticker, sell_price, sell_amount, sell_date, tax, fee, sector,exchange_rate)
            if response.status_code == 200:
                st.success("매도 기록 등록이 완료했습니다!")
                request_summary = search_box + "에 대한 매도 기록이 등록되었습니다."
                st.info(request_summary)
            else:
                st.error("매도 기록 등록이 실패했습니다!")
                st.stop()
