import streamlit as st
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


# Create an empty container
actual_email = "email"
actual_password = "password"

# login() function access to database server and check username and password exist
def login(username, password):
    # TODO : remove this
    return True
    if username == actual_email and password == actual_password:
        return True
    return False

def show_main_page():
    with mainSection:
        st.title("Portfolio Service")
        st.success("Login successful")
        show_pages(
            [
                Page("pages/1_Portfolio.py", "Portfolio", "💸"),
                Page("pages/2_Trading_Journal.py", "Trading Journal", "📝"),
                Page("pages/3_Monthly_trade.py", "Monthly Trade", "📈️"),
                Page("pages/4_Daily_News.py", "Daily News", "📰"),
                Page("pages/5_My_Watchlist.py", "My Watchlist", "👀"),
                Page("pages/6_AI_Assistant.py", "AI Asisstant", "🤖"),
            ]
        )
        hide_pages(
            [
                Page("pages/login_page.py", "Login Page", "🏠"),
                Page("pages/sign_in_page.py", "Sign in", "🧑"),
                Page("pages/find_password_page.py", "Find Password", "🔑"),
            ]
        )

def logout_btn_clicked():
    st.session_state[loginSessionState] = False
def show_logout_page():
    logoutSection.empty()
    with logoutSection:
        st.button("Log out", key="logout",on_click=logout_btn_clicked)
        st.sidebar.button("Log out", key="logout_sidebar",on_click=logout_btn_clicked)

# loginBtnClicked() function handle when login butten clicked case
def login_btn_clicked(email, password):
    if login(email, password):
        st.session_state[loginSessionState] = True
    else:
        st.session_state[loginSessionState] = False
        st.error("Invalid User")

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
        show_login_page()
    else:
        if st.session_state[loginSessionState]:
            show_logout_page()
            show_main_page()
        else:
            show_login_page()




