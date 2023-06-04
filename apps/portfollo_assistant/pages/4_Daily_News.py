import streamlit as st

usernameSession = 'username'
userSession = st.session_state[usernameSession]


st.markdown("# Daily News 📰")
st.sidebar.markdown("# Daily News 📰")

st.sidebar.success("Daily News 📰")
st.sidebar.info("여기는 매일 이슈에 대해서 정리해줄 페이지입니다.")
st.sidebar.title("Daily News 📰")
st.sidebar.markdown(
    """
    다음은 본 페이지의 요구사항입니다.    

    - 포트폴리오와 관련된 뉴스를 보여준다.
    - 관심종목과 관련된 뉴스를 보여준다.
    """
)
