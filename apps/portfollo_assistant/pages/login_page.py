import streamlit as st
import requests
from st_pages import show_pages, Page, hide_pages

st.set_page_config(
    page_title="Portfolio Assistant",
    page_icon="👋",
)

headerSection = st.container()
loginSection = st.container()
mainSection = st.container()
logoutSection = st.container()

loginSessionState = 'loggedIn'
usernameSession = 'username'

def show_main_page():
    with mainSection:
        st.title("Portfolio Service")
        show_pages(
            [
                Page("pages/1_Portfolio.py", "My Stocks", "💸"),
                Page("pages/2_Trading_Journal.py", "Trading Journal", "📝"),
                Page("pages/3_Monthly_trade.py", "Monthly Trade", "📈️"),
                Page("pages/4_Daily_News.py", "Daily News", "📰"),
                Page("pages/5_My_Watchlist.py", "My Watchlist", "👀"),
                Page("pages/6_AI_Assistant.py", "AI Asisstant", "🤖"),
                Page("pages/7_Buy_and_sell_records.py", "Buy Sell Records", "➕"),
            ]
        )
        hide_pages(
            [
                Page("pages/login_page.py", "Login Page", "🏠"),
                Page("pages/sign_in_page.py", "Sign in", "🧑"),
                Page("pages/find_password_page.py", "Find Password", "🔑"),
            ]
        )


# login() function access to database server and check username and password exist
def login(email, password):
    response = requests.post('http://localhost:9000/login',
                             json={'email': email, 'password': password})
    print("login response: ", response)
    if response.status_code == 200:
        return True
    else:
        return False
    # session state를 바깥에서 변경할 수 있는지 확인해보기
    # session state 기반으로 데이터 출력하기
    # st.session_state["username"] = username


def logout_btn_clicked():
    st.session_state[loginSessionState] = False
    st.session_state[usernameSession] = None
    st.success("User logged out successfully")

def show_logout_page():
    logoutSection.empty()
    with logoutSection:
        st.button("Log out", key="logout",on_click=logout_btn_clicked)
        st.sidebar.button("Log out", key="logout_sidebar",on_click=logout_btn_clicked)


def login_btn_clicked(email, password):
    if login(email, password):
        st.session_state[loginSessionState] = True
        st.session_state[usernameSession] = email
        st.success("logged in successfully")
    else:
        st.session_state[loginSessionState] = False
        st.session_state[usernameSession] = None
        st.error("Failed to login")
def show_login_page():
    with loginSection:
        st.markdown("#### Login ")
        if st.session_state[loginSessionState] == False:
            email = st.text_input("Email",placeholder="Enter your email")
            password = st.text_input("Password",placeholder="Enter password" ,type="password")
            st.button("Login",on_click=login_btn_clicked, args=(email, password))


with headerSection.form("login"):
    if loginSessionState not in st.session_state:
        st.session_state[loginSessionState] = False
        st.session_state[usernameSession] = None
        show_login_page()
    else:
        if st.session_state[loginSessionState]:
            show_logout_page()
            show_main_page()
        else:
            show_login_page()




