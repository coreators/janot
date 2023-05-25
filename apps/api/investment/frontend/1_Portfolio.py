import streamlit as st
import requests

st.set_page_config(
    page_title="My Portfolio",
    page_icon="👋",
)
total, korea, usa, crypto= st.tabs(['Total', 'Korea', 'USA','Crypto'])

with total:
    st.title("All Accounts")

with korea:
    st.title("Korea Accounts")

with usa:
    st.title("USA Accounts")

with crypto:
    st.title("Crypto Accounts")


st.markdown("# Main page 🎈")
st.sidebar.success("Main page 🎈")
st.sidebar.info("여기는 메인 페이지입니다.포트폴리오를 여기다가 구현할 예정입니다.")
st.sidebar.title("Main page 🎈")

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
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)