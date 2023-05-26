import streamlit as st
import requests

st.set_page_config(
    page_title="My Portfolio",
    page_icon="👋",
)
total, korea, usa, dollar= st.tabs(['Total', 'Korea', 'USA','Dollar'])

with total:
    st.title("All Accounts")

with korea:
    st.title("Korea Accounts")

with usa:
    st.title("USA Accounts")
    # 샀을때의 환율
    # 기존에 가지고 있던 달러로 했으면 그대로 써주기



st.markdown("# Main page 🎈")
st.sidebar.success("Main page 🎈")
st.sidebar.info("여기는 메인 페이지입니다.포트폴리오를 여기다가 구현할 예정입니다.")
st.sidebar.title("Main page 🎈")
st.sidebar.button("포트폴리오 그래프")
st.sidebar.checkbox("현재 포트폴리오의 종목별 비중")
st.sidebar.checkbox("현재 포트폴리오의 국가별 비중")
st.sidebar.checkbox("현재 포트폴리오의 자산별 비중")
st.sidebar.button("포트폴리오 수익률")



st.sidebar.markdown(
    """
    여기는 메인페이지입니다. 포트폴리오를 여기다가 구현할 예정입니다.
    환율정보를 가져오는 API를 사용하였습니다.
    본 페이지는 매매일지를 기반으로 결과를 출력만합니다.
    
    아래는 Optional한 기능들입니다.
    - 질문 요구페이지 추가
    - 모듈화 가능하게
    - 예금 포함
    - 주가 위치별 메모
    - 실제 계좌정보 가져올 수도 있는 가능성 부여
    - Gpt검색서비스 추가
    - 연수익률 그래프
    - 연 투자금액에 따른 해당 수익률 (의미가있나?)
    - 배당금 그래프
    """
)
st.markdown(
    """
    포트폴리오 그래프 
    
    - 현재 포트폴리오의 종목별 비중 (etc는 너무 작을때 그냥 무시)
    - 현재 포트폴리오의 분야별 비중
    - 현재 포트폴리오의 국가별 비중
    - 현재 포트폴리오의 자산별 비중
    
    
    종목명	매매 시작일	보유수량	평균단가	총 투자금	현재주가	평가 수익률	평가 손익	평가금액	"매매 비용
    
    (수수료+제세금)"	실현 수익률	실현손익	종목 설명	비중	포트	52주 최고점 ($)	고점대비 하락률
	
	자산비중							
    현금	100%		평가 손익합			달러당 환율	
    주식	0%		
    채권	0%
    한국주식
    미국주식
    """
)