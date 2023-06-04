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


st.markdown("# Trading Journal")
st.sidebar.markdown("# Trading Journal")

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

with total:
    st.empty()
    st.title("All Accounts")

with korea:
    st.title("Korea Accounts")

with usa:
    st.empty()
    st.title("USA Accounts")