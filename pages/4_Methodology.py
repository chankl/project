import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="Buying HDB flat in the resale market"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Methodology")

st.subheader("Chatbot With Information")

st.write(f"**Step 1:** We compiled a list of URLs from official HDB web pages that are relevant to buying a resale HDB flat.")
st.write(f"**Step 2:** Using the crewAI tool called 'WebsiteSearchTool', we scrapped the web pages and stored the embeddings into an sqlite3 database.")         
st.write(f"**Step 3:** Receive the query from the user.")
st.write(f"**Step 4:** Two AI agents are used to process the query")
st.markdown("- Research Analyst conducts in-depth research on the query using the scrapped data and its previous response.")
st.markdown("- Customer Service Agent answers customer's question based on the research report.")
st.image("./images/use_case_1.webp", caption="Process flow for Chatbot.")

st.subheader("Historical Resale Flat Price Analyser")

st.write(f"**Step 1:** We downloaded the official historical resale flat price data (2017 onwards) from https://data.gov.sg.")
st.write(f"**Step 2:** Display the table in the app and insert widgets to allow the user to interactively filter the data based on one or more columns.")
st.write(f"**Step 3:** Upon clicking the 'Analyse' button, an AI agent is used to analyse the filtered data and generate a comprehensive analysis report.")
st.markdown("- Content Planner uses a custom pandas_tool to analyse the data and generate the report. This report can be used to advise someone who is planning to buy a resale flat.")
st.image("./images/use_case_2.webp", caption="Process flow for Analyser.")
