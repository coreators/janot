import streamlit as st
from st_pages import show_pages, Page, hide_pages

# Create an empty container
st.title("Portfolio Service")
placeholder = st.empty()

actual_email = "email"
actual_password = "password"

with placeholder.form("login"):
    st.markdown("#### Login ")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")


if submit and email == actual_email and password == actual_password:
    # If the form is submitted and the email and password are correct,
    # clear the form/container and display a success message
    placeholder.empty()
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

elif submit and email != actual_email and password != actual_password:
    st.error("Login failed")
else:
    pass


