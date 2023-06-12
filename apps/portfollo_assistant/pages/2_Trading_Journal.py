import streamlit as st
from pydantic import BaseModel, Field
import streamlit_pydantic as sp
from streamlit_searchbox import st_searchbox
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from backend.schemas import KorJournalCreate
from pathlib import Path
import pandas as pd
import requests
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode , ColumnsAutoSizeMode

usernameSession = 'username'
userSession = st.session_state[usernameSession]


st.markdown("# Trading Journal")
st.sidebar.markdown("# Trading Journal")
st.write(userSession + " hello!")

buy_or_sell = st.sidebar.selectbox("매수 매도 선택", ["매수", "매도"])

korea, usa, dollar= st.tabs(['Korea', 'USA',"Dollar"])
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

kor_list = pd.read_csv("resources/kor_ticker_list.csv")
usa_list = pd.read_csv("resources/usa_ticker_list.csv")


# 유저의 모든 데이터를 긁어와서 화면에 표시해주기
@st.cache_data()
def fetch_data():
    response = requests.get('http://localhost:9000/api/v1/journal/kor/read',
                             json={'email': userSession})
    print("fetch data : ", response , "user name : ",userSession)

    # 0. email에 해당하는 매수/매도 데이터들 다 긁어오기
    df = pd.DataFrame(response.json())


    # 1. 날짜를 내림차순으로 정렬
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df = df.sort_values(by=['date'], ascending=False)

    df = df.rename(columns={
        "ticker": "종목명",
        "price": "가격",
        "amount": "수량",
        "date": "매수/매도 일자",
        "fee": "수수료",
        "tax": "세금",
        "sector": "섹터",
        "is_buy": "매수/매도",
        "profit_loss":"매도 손익"})
    name_dict = kor_list.set_index('Code').to_dict()['Name']



    # 2. Ticker로 저장된 DB값을 종목명으로 치환해주고, True/False를 매수/매도로 치환해줌.
    df['종목명'] = df['종목명'].map(name_dict).fillna(df['종목명'])
    df['매수/매도'] = df['매수/매도'].map({True: "매수", False: "매도"})

    # 3. 기존 인덱스를 삭제하고 종목명으로 인덱스 설정
    df.set_index('종목명',inplace=True)

    # 4. 출력 필요없는 항목들 제거
    del df['transaction_id']
    del df['세금']
    del df['수수료']
    del df['sold_amount']

    # 5. 가격에 원화 붙여줌
    df['가격'] = df['가격'].apply(lambda x: str(x) + '원')
    df['매도 손익'] = df['매도 손익'].apply(lambda x: str(x) + '원')

    if response.status_code == 200:
        return df
    else:
        return pd.DataFrame()

@st.cache_data()
def fetch_data_usa():
    response = requests.get('http://localhost:9000/api/v1/journal/usa/read',
                            json={'email': userSession})
    print("fetch data : ", response , "user name : ",userSession)

    # 0. email에 해당하는 매수/매도 데이터들 다 긁어오기
    df = pd.DataFrame(response.json())


    # 1. 날짜를 내림차순으로 정렬
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df = df.sort_values(by=['date'], ascending=False)

    df = df.rename(columns={
        "ticker": "종목명",
        "price": "가격",
        "amount": "수량",
        "date": "매수/매도 일자",
        "fee": "수수료",
        "tax": "세금",
        "sector": "섹터",
        "is_buy": "매수/매도",
        "exchange_rate":"환율",
        "profit_loss":"매도 손익",
        "profit_loss_with_exchange":"환전 포함 매도 손익"})
    name_dict = kor_list.set_index('Code').to_dict()['Name']

    # 2. Ticker로 저장된 DB값을 종목명으로 치환해주고, True/False를 매수/매도로 치환해줌.
    df['종목명'] = df['종목명'].map(name_dict).fillna(df['종목명'])
    df['매수/매도'] = df['매수/매도'].map({True: "매수", False: "매도"})

    # 3. 기존 인덱스를 삭제하고 종목명으로 인덱스 설정
    df.set_index('종목명',inplace=True)

    # 4. 출력 필요없는 항목들 제거
    del df['transaction_id']
    del df['세금']
    del df['수수료']
    del df['sold_amount']

    # 5. 달러/원화 표시 추가
    df['가격'] = df['가격'].apply(lambda x: str(x) + '$')
    df['매도 손익'] = df['매도 손익'].apply(lambda x: str(x) + '$')
    df['환율'] = df['환율'].apply(lambda x: str(x) + '원')
    df['환전 포함 매도 손익'] = df['환전 포함 매도 손익'].apply(lambda x: str(x) + '원')
    if response.status_code == 200:
        return df
    else:
        return pd.DataFrame()

def create_table(df):
    st.dataframe(df,use_container_width=True)


with korea:
    st.title("Korea Accounts")
    df=fetch_data()
    create_table(df)


with usa:
    st.empty()
    st.title("USA Accounts")
    df=fetch_data_usa()
    create_table(df)