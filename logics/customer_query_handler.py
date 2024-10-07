import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import WebsiteSearchTool
from langchain.agents import Tool
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

# Load the environment variables
# If the .env file is not found, the function will return `False
if load_dotenv('.env'):
    OPENAI_KEY = os.getenv('OPENAI_API_KEY')
else:
    OPENAI_KEY = st.secrets['OPENAI_API_KEY']

urls = [
    "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats",
    "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats/overview",
    "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats/plan-source-and-contract",
    "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats/plan-source-and-contract/planning-considerations",
    "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats/plan-source-and-contract/planning-considerations/managing-the-flat-purchase",
    "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats/plan-source-and-contract/planning-considerations/eip-spr-quota",
    "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats/plan-source-and-contract/planning-considerations/conversion-scheme-application-procedure",
    "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats/plan-source-and-contract/mode-of-financing",
    "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats/plan-source-and-contract/option-to-purchase",
    "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats/plan-source-and-contract/request-for-value",
    "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats/resale-application",
    "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats/resale-application/application",
    "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats/resale-application/acceptance-and-approval",
    "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats/resale-application/request-for-enhanced-contra-facility",
    "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats/resale-completion",
    "https://www.hdb.gov.sg/residential/buying-a-flat/conditions-after-buying",
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/finding-a-flat?anchor=resale-flat",
    "https://www.hdb.gov.sg/cs/infoweb/hdb-flat-portal/HFE/get-help",
    "https://www.hdb.gov.sg/cs/infoweb/hdb-flat-portal/HFE/get-help/general",
    "https://www.hdb.gov.sg/cs/infoweb/hdb-flat-portal/HFE/get-help/submission-of-an-hfe-letter-application",
    "https://www.hdb.gov.sg/cs/infoweb/hdb-flat-portal/HFE/get-help/HFE-letter-application-process",
    "https://www.hdb.gov.sg/cs/infoweb/hdb-flat-portal/HFE/get-help/integrated-housing-loan-application-service",
    "https://www.hdb.gov.sg/cs/infoweb/hdb-flat-portal/HFE/get-help/outcome-of-HFE-letter-application",
    "https://www.hdb.gov.sg/residential/buying-a-flat/finding-a-flat/resale-seminars",
]

# Create a new instance of the WebsiteSearchTool
for url in urls:
    tool_websearch = WebsiteSearchTool(url)

# <---------------------------------- Creating Agents ---------------------------------->
agent_researcher = Agent(
    role="Research Analyst",
    goal="Conduct in-depth research on the topic: {topic}",
    backstory="""You're working on conducting in-depth research on the topic: {topic}.
    You are given some context from previous replies: {history}.
    Only use the data provided by the web search tool and the context {history} to gather the necessary information.""",

    allow_delegation=False,
    verbose=False,
)

agent_writer = Agent(
    role="Customer Service Agent",
    goal="Answer customer's question about the topic: {topic}",
    backstory="""You are a helpful customer service agent chatbot. User has a question about the topic: {topic}.
    You base your answer on the outline from the research report from the Research Analyst.
    If there is no available information for the {topic}, inform customer that you can only answer questions related to buying a HDB flat in the resale market.""",

    allow_delegation=False, 
    verbose=False,
)

# <---------------------------------- Creating Tasks ---------------------------------->
task_research = Task(
    description="""\
    1. Conduct in-depth research on the topic: {topic}
    2. Include the context from {history} in the research if it is relevant to {topic}.
    3. Your research findings must be related to buying a HDB flat in the resale market.
    4. If {topic} is not relevant to buying a HDB flat in the resale market, immediately inform the Customer Service Agent that there is no available information for the {topic}.""",

    expected_output="""\
    A detailed research report with information on the topic.""",

    agent=agent_researcher,
    tools=[tool_websearch],
)

task_write = Task(
    description="""\
    1. Use the research report from the Research Analyst to generate the answer for the customer's query on {topic}.
    2. Keep the answer concise, accurate and factual. Use numbered bullets if there are multiple points. Include a brief introduction and brief conclusion.
    3. Answer the customer in a courteous and professional manner.
    4. Do not write the answer in the form of a written email reply.
    5. Proofread for grammatical errors and align to the common style used in chatbots.
    6. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    7. If {topic} is not relevant to buying a HDB flat in the resale market, just explain that you can only answer questions related to buying a HDB flat in the resale market.""",

    expected_output="""\
    A well-written reply in markdown format.""",

    agent=agent_writer
)

# <---------------------------------- Creating the Crew ---------------------------------->
crew = Crew(
    agents=[agent_researcher, agent_writer],
    tasks=[task_research, task_write], 
    verbose=False
)

# <---------------------------------- Running the Crew ---------------------------------->
def process_user_message(chat_history, user_input):
    result = crew.kickoff(inputs={"history": chat_history, "topic": user_input})
    final_text = result.raw.replace('$', '\\$')

    #print(f"Final markdown text: {final_text}")
    return final_text

# This function provides widgets for filtering a dataframe. Code taken from https://github.com/tylerjrichards/st-filter-dataframe
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

def process_table(df):

    pandas_tool_agent = create_pandas_dataframe_agent(
        llm=ChatOpenAI(temperature=0, model='gpt-4o-mini'),
        df=df, 
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code=True
    )

    # Create the tool
    pandas_tool = Tool(
        name="Manipulate and Analyze tabular data with Code",
        func=pandas_tool_agent.invoke,
        description="Useful for search-based queries",
    )

    # Creating Agents
    agent_data_analyst = Agent(
        role="Content Planner",
        goal="Analyze the provided data. Provide any useful information derived from the data that would help someone who is planning to buy a resale flat.",
        backstory="""You're the best data analyst.""",
        allow_delegation=False,
        verbose=False,
        tools=[pandas_tool],
    )

    task_analyze = Task(
        description="""\
        1. Use the tool to analyze the provided data. The data contains historical resale flat prices in Singapore dollars.
        2. Develop a comprehensive report using only information from the provided data.
        3. The report will be read by the customer directly. Do not include further instructions or next steps.
        3. Do not include code or plots.""",

        expected_output="""\
        A comprehensive analysis report that presents insights from the provided data. Make sure to only use the filtered data to generate the report.""",

        agent=agent_data_analyst,
    )

    # Creating the Crew
    crew2 = Crew(
        agents=[agent_data_analyst],
        tasks=[task_analyze],
        verbose=False
    )

    result = crew2.kickoff()
    final_text = result.raw.replace('$', '\\$')

    #print(f"Final markdown text: {final_text}")
    return final_text