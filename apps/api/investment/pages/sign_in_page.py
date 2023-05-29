import streamlit as st

placeholder = st.empty()

with placeholder.form("sign_in"):
    st.empty()
    st.markdown("#### Sign In ")
    sign_in_email = st.text_input("Email")
    sign_in_name = st.text_input("Name")
    sign_in_password = st.text_input("Password", type="password")
    sign_in_password_check = st.text_input("Check Password", type="password")
    sign_in_submit = st.form_submit_button("Submit")