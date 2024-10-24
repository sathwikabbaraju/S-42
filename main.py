import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
import os

# Set up the working directory
pwd = os.getcwd()

# Initialize the ChatOpenAI model
llm = ChatOpenAI(model="gpt-4o")

# Streamlit app title
st.title("CHAT WITH YOUR EXCEL FILE")

# File uploader for Excel files
file = st.file_uploader("Upload your file", type=["xlsx"])

if file:
    try:
        # Load the Excel file
        df = pd.read_excel(file)

        # Drop any unnamed columns (e.g., index columns)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Ensure DataFrame is valid
        if df.empty:
            st.error("The uploaded file is empty. Please upload a valid Excel file.")
        else:
            # Display DataFrame info for debugging
            st.write("DataFrame Info:")
            st.write(df.info())

            # Display the DataFrame to understand its structure
            st.write("DataFrame Preview:")
            st.dataframe(df)  # Display the DataFrame in the Streamlit app

            # Convert all DataFrame data to string, handling mixed types
            df = df.applymap(lambda x: str(x) if pd.notnull(x) else '')  # Convert all data to string

            # Display the data types of each column for debugging
            st.write("Data Types:")
            st.write(df.dtypes)

            # Chat functionality
            input_text = st.text_area("Ask your question about the data here")
            if st.button("Submit"):
                # Prepare the context for the chat
                context = df.to_string(index=False)  # Get string representation of the DataFrame
                prompt = f"You have the following data:\n{context}\n\nQuestion: {input_text}\nAnswer:"

                # Get response from the language model
                response = llm.chat(prompt)
                st.write(response)

    except Exception as e:
        # Display error message
        st.error(f"An error occurred: {e}")
