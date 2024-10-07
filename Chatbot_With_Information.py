# Set up and run this Streamlit App
import streamlit as st
from logics.customer_query_handler import process_user_message
from helper_functions.utility import check_password

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="Buying HDB flat in the resale market"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Chatbot with information on buying a resale HDB flat")

# Check if the password is correct.  
if not check_password():  
    st.stop()

# Initialization
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = ''

form = st.form(key="form")
form.subheader("Ask me anything related to buying a HDB flat in the resale market!👋🤖")

user_prompt = form.text_area("Enter your prompt here", height=200)

if form.form_submit_button("Submit"):
    
    st.toast(f"User Input Submitted - {user_prompt}")

    st.divider()

    response = process_user_message(st.session_state['chat_history'], user_prompt)
    st.write(response)

    st.session_state['chat_history'] = response

with st.expander("Disclaimer"):

    st.write(f"**IMPORTANT NOTICE**: This web application is a prototype developed **for educational purposes only**. The information provided here is **NOT intended for real-world usage** and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.")

    st.write(f"**Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.**")

    st.write(f"Always consult with qualified professionals for accurate and personalized advice.")