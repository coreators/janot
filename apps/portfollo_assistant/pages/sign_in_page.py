import streamlit as st
import requests

usernameSession = 'username'
userSession = st.session_state[usernameSession]


placeholder = st.empty()

def sign_in_request(email, username, password):
    response = requests.post('http://localhost:9000/register',
                             json={'username': username, 'password': password, 'email': email})
    return response



with placeholder.form("sign_in"):
    st.empty()
    st.markdown("#### Sign In ")
    sign_in_email = st.text_input("Email")
    sign_in_name = st.text_input("Name")
    sign_in_password = st.text_input("Password", type="password")
    sign_in_password_check = st.text_input("Check Password", type="password")
    sign_in_submit = st.form_submit_button("Submit")
    if sign_in_submit:
        if sign_in_password == sign_in_password_check:
            response = sign_in_request(sign_in_email, sign_in_name, sign_in_password)
            if response.status_code == 200:
                st.success("User registered successfully")
            else:
                st.error("Failed to register user")
            st.stop()
        else:
            st.error("Password does not match")
            st.stop()