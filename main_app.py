import streamlit as st
import os
import requests
import pandas as pd
import re
from utils import *
from scrap_search import *

# Title of the app
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>CSV Column Extractor with Custom Prompt</h1>", unsafe_allow_html=True)
print(st.session_state)
if "groq_authenticated" not in st.session_state:
    st.session_state["groq_authenticated"] = False

if "scraper_authenticated" not in st.session_state:
    st.session_state["scraper_authenticated"] = False
print(st.session_state)    
    
# Step 1: API Key Input and Authentication (displayed only if not authenticated)
if not st.session_state["groq_authenticated"]:
    st.markdown("### Step 1: Authenticate with Groq API Key")
    api_key = st.text_input("Enter your Groq API Key:", type="password")

    if st.button("Authenticate Groq"):
        if api_key:
            # Attempt to authenticate the key with a sample request
            os.environ["GROQ_API_KEY"]=api_key
            if authenticate_groq_api()==1:
                st.success("API key authenticated successfully.")
                st.session_state["groq_authenticated"] = True 
                # st.session_state.clear()
            else:
                st.error(f"Error while connecting to Groq API. ")
        else:
            st.error("Please enter your API key.")
            
# Step 1: API Key Input and Authentication (displayed only if not authenticated)
if not st.session_state["scraper_authenticated"]:
    
    st.markdown("### Step 2: Authenticate with Scraper API Key")
    api_key = st.text_input("Enter your Scraper API Key:", type="password")

    if st.button("Authenticate Scraper"):
        if api_key:
            # Attempt to authenticate the key with a sample request
            os.environ["SCRAPER_API_KEY"]=api_key
            if authenticate_scraper_api()==1:
                st.success("API key authenticated successfully.")
                st.session_state["scraper_authenticated"] = True 
                # st.session_state.clear()
            else:
                st.error(f"Error while connecting to Scrapper API. ")
        else:
            st.error("Please enter your API key.")

# Step 2: CSV Upload and Prompt Customization (only accessible if authenticated)
if st.session_state["groq_authenticated"] and st.session_state["scraper_authenticated"]:
    # Upload CSV file
    # st.session_state.clear()
    st.markdown("### Step 3: Upload and Configure CSV Data")
    uploaded_file = st.file_uploader("📂 Upload your CSV file here", type="csv")

    if uploaded_file is not None:
        # Read the file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame with a heading
        st.markdown("### Preview of Uploaded Data")
        st.dataframe(df)

        # Guide the user on creating a custom prompt
        st.markdown("#### Define a Custom Prompt")
        st.write("Write a prompt to extract specific data from your CSV file. Use `{column_name}` as a placeholder for columns in your dataset.")
        
        # Example prompt
        st.info("Example prompt: `Get me the email address of {company}.`")

        # Text input for custom prompt
        custom_prompt = st.text_area("Enter your custom prompt:", placeholder="e.g., Get me the email address of {company}.")

        if custom_prompt:
            # Extract column name from the placeholder in the custom prompt
            match = re.search(r"{(.*?)}", custom_prompt)
            st.write(match.group(1))
            if match:
                column_name = match.group(1)  # Extracted column name

                # Check if the extracted column name exists in the dataframe
                if column_name in df.columns:
                    # Generate prompts by replacing placeholder with each value in the column
                    ops=(getResponseFromSheet(custom_prompt=custom_prompt,df=df.iloc[:5],column_name=column_name))
                    # generated_prompts = [custom_prompt.replace(f"{{{column_name}}}", str(value)) for value in df[column_name]]
                    
                    # # Display generated prompts
                    # st.markdown("### Generated Prompts:")
                    for prompt in ops:
                        st.write(f"- {prompt}")
                else:
                    st.error(f"Column '{column_name}' not found in the CSV. Please check the column name in your prompt.")
            else:
                st.error("No valid column placeholder found in your prompt. Use `{column_name}` to specify the column.")
    else:
        st.markdown("<p style='text-align: center; color: #FF5722;'>Please upload a CSV file to get started.</p>", unsafe_allow_html=True)
