import streamlit as st
import pandas as pd

# Title of the app with some styling
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>CSV Column Extractor with Custom Prompt</h1>", unsafe_allow_html=True)

# Upload CSV file
uploaded_file = st.file_uploader("📂 Upload your CSV file here", type="csv")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display the DataFrame with a heading
    st.markdown("### Step-1: Preview of Uploaded Data")
    st.dataframe(df)

    # Guide the user on creating a custom prompt
    st.markdown("#### Step-2: Define a Custom Prompt")
    st.write("Write a prompt to extract specific data from your CSV file. Use `{column_name}` as a placeholder for columns in your dataset.")
    
    # Example prompt
    st.info("Example prompt: `Get me the email address of {company}.`")

    # Text input for custom prompt
    custom_prompt = st.text_input("Enter your custom prompt:", placeholder="e.g., Get me the <required-data> of {<desired-column>}.")

    # Display chosen prompt if available
    if custom_prompt:
        st.markdown("### Your Custom Prompt:")
        st.write(f"**{custom_prompt}**")
else:
    # Display a message when no file is uploaded
    st.markdown("<p style='text-align: center; color: #FF5722;'>Please upload a CSV file to get started.</p>", unsafe_allow_html=True)
