import streamlit as st
from time import sleep
from st_pages import Page, hide_pages
import requests

API_URL = 'http://127.0.0.1:5000/'

def authenticate(username, password):
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(f'{API_URL}/login', json=data)
    return response

def user_login(uname, passwd):
    response = authenticate(uname, passwd)
    if response.status_code == 200:
        return True
    else:
        st.write("Incorrect username or password")
        return False

# Streamlit layout
_, img, _ = st.columns(3)
st.title('      Library Managment System')
with img:
    st.image('data/image.png', width=200)
st.title('Login')

# Input fields for username and password
username = st.text_input('Username')
password = st.text_input('Password', type='password')


if st.button('Login'):
    if user_login(username, password):
        st.success('Login successful!')
        st.switch_page("./pages/main.py")
        hide_pages(
            [Page("login.py"),
            Page("pages/main.py")]
            )
    else:
        st.error('Invalid username or password. Please try again.')




