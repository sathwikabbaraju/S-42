import streamlit as st
from pymongo import MongoClient
import pandas as pd
from crewai import Crew, Agent, Task
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv


load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
#openai_api_key = st.secrets["OPENAI_API_KEY"]
#chromadb==0.5.15
# Initialize Streamlit app
st.title("Project S-42")
st.subheader("Ask questions about BOQ's (BMS) data")

# Step 1: Connect to MongoDB and Fetch Data (done only once)
@st.cache_resource
def fetch_data_from_mongo():
    client = MongoClient("mongodb+srv://abbarajusatwik:w6ut5cMcwivjbWcb@alpha.zlw5j.mongodb.net/preAlpha?retryWrites=true&w=majority")
    db = client['preAlpha']
    collection = db['BMS']
    cursor = collection.find()
    data = list(cursor)
    df = pd.DataFrame(data)
    return df

excel_data = fetch_data_from_mongo()

# Step 2: Define the Research Agent (LLM Setup)
researcher = Agent(
    role="Senior Research Assistant",
    goal="Conduct comprehensive analysis based on user questions about Excel data.",
    backstory="""You work as a data analyst. Your expertise lies in analyzing and summarizing data from various sources.
    You have a knack for transforming data insights into understandable narratives.""",
    verbose=False,
    allow_delegation=False,
    llm=ChatOpenAI(
        model_name="gpt-4o",
        temperature=0.2,
        openai_api_key=os.environ['OPENAI_API_KEY']
    )
)

# Step 3: Handle User Questions and Use Data
def handle_user_question(question, data):
    task = Task(
        description=f"User question: {question}\n\nData: {data.to_dict()}",  
        expected_output="A detailed analysis and insights based on the given question.",
        agent=researcher
    )

    crew = Crew(
        agents=[researcher],
        tasks=[task],
        verbose=1
    )

    result = crew.kickoff()
    return result

# Step 4: Streamlit Chat Interface
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input for user question
user_input = st.text_input("Enter your question:", "")

if st.button("Submit") and user_input:
    answer = handle_user_question(user_input, excel_data)
    st.session_state.chat_history.append({"question": user_input, "answer": answer})

# Display chat history
for chat in st.session_state.chat_history:
    st.write(f"**👨🏻‍💻You:** {chat['question']}")
    st.write(f"**🤖Bot:** {chat['answer']}")



# import streamlit as st
# import pandas as pd
# from pymongo import MongoClient
# from crewai import Crew, Agent, Task
# from langchain_openai import ChatOpenAI
# import os,glob

# # Step 1: Connect to MongoDB and Fetch Data
# def fetch_data_from_mongo():
#     client = MongoClient("mongodb+srv://abbarajusatwik:w6ut5cMcwivjbWcb@alpha.zlw5j.mongodb.net/preAlpha?retryWrites=true&w=majority")
#     db = client['preAlpha']  # Database name
#     collection = db['BMS']   # Collection name

#     cursor = collection.find()  # Fetch all documents
#     data = list(cursor)

#     # Convert to DataFrame
#     df = pd.DataFrame(data)
#     return df

# # Step 2: Define the Research Agent (LLM Setup)
# def create_researcher():
#     researcher = Agent(
#         role="Senior Research Assistant",
#         goal="Conduct comprehensive analysis based on user questions about Excel data.",
#         backstory="""You work as a data analyst. Your expertise lies in analyzing and summarizing data from various sources.
#         You have a knack for transforming data insights into understandable narratives.""",
#         verbose=False,
#         allow_delegation=False,
#         llm=ChatOpenAI(
#             model_name="gpt-4o",
#             temperature=0.2,
#             openai_api_key=os.environ['OPENAI_API_KEY']  # Ensure API key is set in the environment
#         )
#     )
#     return researcher

# # Step 3: Handle User Questions and Use Data
# def handle_user_question(question, data, researcher):
#     # Task description now includes the Excel data from MongoDB
#     task = Task(
#         description=f"User question: {question}\n\nData: {data.to_dict()}",
#         expected_output="A detailed analysis and insights based on the given question.",
#         agent=researcher
#     )

#     crew = Crew(
#         agents=[researcher],
#         tasks=[task],
#         verbose=1
#     )

#     result = crew.kickoff()
#     return result

# # Step 4: Streamlit Frontend
# st.title("Project S-42")

# # Button to load data from MongoDB
# if st.button("Load Data from MongoDB"):
#     st.write("Fetching data...")
#     excel_data = fetch_data_from_mongo()
#     st.write("Data Loaded:")
#     st.write(excel_data.head())  # Display first few rows of the fetched data

# # Text input for user question
# user_input = st.text_input("Ask a question about the data:")

# # If the user provides a question
# if user_input and 'excel_data' in locals():
#     researcher = create_researcher()  # Create the LLM agent
#     st.write("Processing your question...")
#     answer = handle_user_question(user_input, excel_data, researcher)
#     st.write("Answer:", answer)
# else:
#     st.write("Please load the data and enter a question.")


# import streamlit as st
# import pandas as pd
# from pymongo import MongoClient
# from crewai import Crew, Agent, Task
# from langchain_openai import ChatOpenAI
# import os, glob

# # Step 1: Connect to MongoDB and Fetch Data
# def fetch_data_from_mongo():
#     client = MongoClient("mongodb+srv://abbarajusatwik:w6ut5cMcwivjbWcb@alpha.zlw5j.mongodb.net/preAlpha?retryWrites=true&w=majority")
#     db = client['preAlpha']  # Database name
#     collection = db['BMS']   # Collection name

#     cursor = collection.find()  # Fetch all documents
#     data = list(cursor)

#     # Convert to DataFrame
#     df = pd.DataFrame(data)
#     return df

# # Step 2: Define the Research Agent (LLM Setup)
# def create_researcher():
#     researcher = Agent(
#         role="Senior Research Assistant",
#         goal="Conduct comprehensive analysis based on user questions about Excel data.",
#         backstory="""You work as a data analyst. Your expertise lies in analyzing and summarizing data from various sources.
#         You have a knack for transforming data insights into understandable narratives.""",
#         verbose=False,
#         allow_delegation=False,
#         llm=ChatOpenAI(
#             model_name="gpt-4o",
#             temperature=0.2,
#             openai_api_key=os.environ['OPENAI_API_KEY']  # Ensure API key is set in the environment
#         )
#     )
#     return researcher

# # Step 3: Handle User Questions and Use Data
# def handle_user_question(question, data, researcher):
#     # Task description now includes the Excel data from MongoDB
#     task = Task(
#         description=f"User question: {question}\n\nData: {data.to_dict()}",
#         expected_output="A detailed analysis and insights based on the given question.",
#         agent=researcher
#     )

#     crew = Crew(
#         agents=[researcher],
#         tasks=[task],
#         verbose=1
#     )

#     result = crew.kickoff()
#     return result

# # Step 4: Streamlit Frontend with Plotting Option
# st.title("Project S-42")

# # Button to load data from MongoDB
# if st.button("Load Data from MongoDB"):
#     st.write("Fetching data...")
#     excel_data = fetch_data_from_mongo()
#     st.write("Data Loaded:")
#     st.write(excel_data.head())  # Display first few rows of the fetched data

# # Options to either chat or generate a plot
# options = ["Chat", "Plot"]
# selected_option = st.selectbox("Choose an option", options)

# # Chat option
# if selected_option == "Chat":
#     user_input = st.text_area("Ask your question here:")
#     if user_input and 'excel_data' in locals():
#         btn = st.button("Submit")
#         if btn:
#             researcher = create_researcher()  # Create the LLM agent
#             st.write("Processing your question...")
#             answer = handle_user_question(user_input, excel_data, researcher)
#             st.write("Answer:", answer)
#     else:
#         st.write("Please load the data and enter a question.")

# # Plot option
# elif selected_option == "Plot":
#     pwd = os.getcwd()  # Current working directory
#     file = glob.glob(pwd + "/*.png")  # Check if there are any plot images in the folder

#     if file:
#         os.remove(file[0])  # Remove any existing plot before generating a new one

#     user_input = st.text_area("Ask a question for plot generation:")
#     if user_input and 'excel_data' in locals():
#         btn = st.button("Submit")
#         if btn:
#             researcher = create_researcher()  # Create the LLM agent for plot-related question
#             response = handle_user_question(user_input, excel_data, researcher)
            
#             # Check if a plot was generated and saved as a .png file
#             file = glob.glob(pwd + "/*.png")
#             if file:
#                 st.image(image=file[0], caption="Plot for: " + user_input, width=1024)
#             else:
#                 st.write("No plot was generated.")
#     else:
#         st.write("Please load the data and enter a plot-related question.")

