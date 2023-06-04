import streamlit as st

usernameSession = 'username'
userSession = st.session_state[usernameSession]

placeholder = st.empty()


with placeholder.form("forget_password"):
    st.empty()
    st.markdown("#### Send Password to Email ")
    email_forget_password = st.text_input("Email")
    submit_forget_password = st.form_submit_button("Submit")