import streamlit as st
import os
import json
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
    st.markdown("### Step 3: Choose Data Source")

    # Let the user choose between uploading a CSV file or entering a Google Sheets link
    data_source = st.radio("Select data source:", ("Upload CSV File", "Enter Google Sheets Link"))
    df=pd.DataFrame()
    flag_to_render_next=False
    if data_source == "Upload CSV File":
        # Display file uploader for CSV
        uploaded_file = st.file_uploader("📂 Upload your CSV file here", type="csv")
        
        if uploaded_file is not None:
            # Read the uploaded file into a DataFrame and display it
            df = pd.read_csv(uploaded_file)
            flag_to_render_next=True
        else:
            st.markdown("<p style='text-align: center; color: #FF5722;'>Please upload a CSV file to get started.</p>", unsafe_allow_html=True)
    elif data_source=="Enter Google Sheets Link":
        json_creds = st.file_uploader("📂 Upload your Service account json credentials here.", type="json")
        if json_creds is not None:
            json_creds=json.load(json_creds)
            google_sheets_url = st.text_input("Enter the Google Sheets link:")
            if google_sheets_url:
                try:
                    df = get_google_sheet(google_sheets_url,json_creds)
                    flag_to_render_next=True
                except Exception as e:
                    st.error(f"Failed to load data from Google Sheets: {e}")
            else:
                st.markdown("<p style='text-align: center; color: #FF5722;'>Please enter spreadsheet link to get started.</p>",unsafe_allow_html=True) 
    
        
    if flag_to_render_next:
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
            if match:
                column_name = match.group(1)  # Extracted column name
                # Check if the extracted column name exists in the dataframe
                if column_name in df.columns:
                    
                    # Generate prompts by replacing placeholder with each value in the column
                    outputs=(getResponseFromSheet(custom_prompt=custom_prompt,df=df,column_name=column_name))
                    df["Generated Outputs"]=outputs
                    data_csv=df.to_csv(index=False)
                    st.download_button(
                        label="Click here to download CSV with added column",
                        data=data_csv,
                        file_name="my_data.csv",
                        mime="text/csv"
                    )
                    st.dataframe(df[[column_name,"Generated Outputs"]])
                    if data_source=="Enter Google Sheets Link":
                        if st.button("Update the Google Sheet"):
                            try:
                                update_google_sheet(google_sheets_url,df,json_creds)
                                st.info("Sheet Updated successfully!")
                            except Exception as e:
                                st.error(f"Some error occured while updating the sheet: {e}")
                            
                else:
                    st.error(f"Column '{column_name}' not found in the CSV. Please check the column name in your prompt.")
            else:
                st.error("No valid column placeholder found in your prompt. Use `{column_name}` to specify the column.")
            

