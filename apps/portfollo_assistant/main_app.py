from st_pages import Page, add_page_title, show_pages
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

show_pages(
    [
        Page("pages/login_page.py", "Login", "🏠"),
        Page("pages/sign_in_page.py", "Sign in", "🧑"),
        Page("pages/find_password_page.py", "Find Password", "🔑"),
    ]
)

add_page_title()  # Optional method to add title and icon to current page
st.title("This is Portfolio Asisstant")
st.error("Please Login")

button = st.button("Login")
if button:
    switch_page("login")