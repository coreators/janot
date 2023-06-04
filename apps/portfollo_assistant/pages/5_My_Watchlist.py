import streamlit as st

usernameSession = 'username'
userSession = st.session_state[usernameSession]


st.markdown("# My Watchlist 👀")
st.sidebar.markdown("# My Watchlist 👀")

st.sidebar.success("My Watchlist 👀")
st.sidebar.info("관심 종목 정리 페이지입니다.")
st.sidebar.title("My Watchlist 👀")
st.sidebar.markdown(
    """
    다음은 본 페이지의 요구사항입니다.    

    - 관심종목 탭을 직접 추가가능한지 확인해보기
    - 관심종목 정리하기
    - 검색기능
    """
)
