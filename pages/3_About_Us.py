import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="Buying HDB flat in the resale market"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About this App")

st.subheader("1. Project Scope")

st.write("This is a Streamlit App developed for AI Champions Bootcamp Project Type C - Capstone Assignment: Building an Interactive LLM-Powered Solution.")

st.subheader("2. Objectives")

st.write("This application enables citizens to interact seamlessly with publicly available information regarding buying a HDB flat in the resale market. \
         It consolidates information and data from multiple official and trustworthy sources, facilitates a deeper understanding through interactive engagements with a chatbot and analyser tool, \
         and presents the relevant information in the way that is customised based on user inputs.")

st.subheader("3. Data sources")

st.markdown("- Policies related to buying a resale HDB flat, scrapped from official web pages within https://www.hdb.gov.sg")
st.markdown("- Resale flat prices based on registration date from Jan-2017 onwards, taken from https://data.gov.sg/datasets/d_8b84c4ee58e3cfc0ece0d773c8ca6abc/view")

st.subheader("4. Features")

st.write(f"**Use case 1:** The chatbot has been trained using policies related to buying a resale HDB flat. Upon receiving a prompt from the user, it will use the last reply and current query \
         to provide an answer to the user. AI agents are used to perform research using web search tools and create the reply to the user.")

st.write(f"**Use case 2:** The analyser provides widgets for the user to filter the historical resale flat price data based on one or more columns. When ready, it then generates a comprehensive \
         analysis report based on the filtered data, providing the user with insights that may help with the purchasing of a resale HDB flat.")

with st.expander("How to use this App"):
    st.write(f"**Chatbot:**")
    st.write("1. Enter your query in the text area.")
    st.write("2. Click the 'Submit' button.")
    st.write("3. The app will generate a reply based on your query.")

    st.write(f"**Analyser:**")
    st.write("1. Use widgets to filter the data.")
    st.write("2. Click the 'Analyse' button.")
    st.write("3. The app will generate an analysis report based on the filtered data.")
