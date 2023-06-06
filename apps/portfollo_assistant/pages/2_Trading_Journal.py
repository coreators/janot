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

kor_list = pd.read_csv("resources/kor_ticker_list.csv")
@st.cache_data()
def fetch_data():
    response = requests.get('http://localhost:9000/api/v1/journal/kor/read',
                             json={'email': userSession})
    print("fecth data : ", response , "user name : ",userSession)
    df = pd.DataFrame(response.json())
    df = df.rename(columns={
        "ticker": "종목명",
        "price": "매수/매도 가격",
        "amount": "수량",
        "date": "매수/매도 일자",
        "fee": "수수료",
        "tax": "세금",
        "sector": "섹터",
        "is_buy": "매수/매도"})
    name_dict = kor_list.set_index('Code').to_dict()['Name']
    # Ticker로 저장된 DB값을 종목명으로 치환해주기
    df['종목명'] = df['종목명'].map(name_dict).fillna(df['종목명'])
    df['매수/매도'] = df['매수/매도'].map({True: "매수", False: "매도"})
    if response.status_code == 200:
        return df
    else:
        return pd.DataFrame()

def create_aggrid_table():
    df = fetch_data()
    gb = GridOptionsBuilder.from_dataframe(df)

    #customize gridOptions
    #gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
    #gb.configure_column("date_only", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='yyyy-MM-dd', pivot=True)
    #gb.configure_column("date_tz_aware", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='yyyy-MM-dd HH:mm zzz', pivot=True)

    #gb.configure_column("apple", type=["numericColumn","numberColumnFilter","customNumericFormat"], precision=2, aggFunc='sum')
    #gb.configure_column("banana", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1, aggFunc='avg')
    #gb.configure_column("chocolate", type=["numericColumn", "numberColumnFilter", "customCurrencyFormat"], custom_currency_symbol="R$", aggFunc='max')


    cellsytle_jscode = JsCode("""
    function(params) {
        if (params.value == 'A') {
            return {
                'color': 'white',
                'backgroundColor': 'darkred'
            }
        } else {
            return {
                'color': 'black',
                'backgroundColor': 'white'
            }
        }
    };
    """)
    gb.configure_column("group", cellStyle=cellsytle_jscode)
    gb.configure_side_bar()
    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()
    AgGrid(df,gridOptions=gridOptions,
           height=1000,
           width='100%',
           columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
           allow_unsafe_jscode=True,
           enable_enterprise_modules=True)



with total:
    st.empty()
    col1, col2, col3 = st.columns(3)
    # 비중을 이런걸로 표시해도 UI가 괜찮을듯
    col1.metric("총 자산", "70 °F", "1.2 °F")
    col2.metric("한국 주식", "9 mph", "-8%")
    col3.metric("미국 주식", "86%", "4%")
    st.title("All Accounts")

with korea:
    st.title("Korea Accounts")
    fetch_data()
    create_aggrid_table()


with usa:
    st.empty()
    st.title("USA Accounts")