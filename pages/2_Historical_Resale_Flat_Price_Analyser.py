import streamlit as st
import pandas as pd
from logics.customer_query_handler import process_table, filter_dataframe
from helper_functions.utility import check_password

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="Buying HDB flat in the resale market"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Historical resale flat prices analyser (Jan-2017 onwards)")

# Check if the password is correct.  
if not check_password():  
    st.stop()

# Load the CSV file as a Pandas DataFrame
df = pd.read_csv("./data/ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv")

filtered_df = filter_dataframe(df)
st.dataframe(filtered_df)

form = st.form(key="form2")
form.subheader("Click Analyse to generate a comprehensive report based on your filtered data!🧮📊")
form.write("Warning: Analysis time depends on the number of returned rows and may take 2-3 minutes on unfiltered data. Please filter as much as possible before clicking analyse.")

if form.form_submit_button("Analyse"):

    st.toast(f"Analysing...")

    st.divider()

    response = process_table(filtered_df)
    st.write(response)

with st.expander("Disclaimer"):

    st.write(f"**IMPORTANT NOTICE**: This web application is a prototype developed **for educational purposes only**. The information provided here is **NOT intended for real-world usage** and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.")

    st.write(f"**Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.**")

    st.write(f"Always consult with qualified professionals for accurate and personalized advice.")