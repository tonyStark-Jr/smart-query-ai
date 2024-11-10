# Smart Query AI

Deployed link: https://smart-query-ai.streamlit.app
Smart Query AI is an interactive Streamlit-based web application that enables users to authenticate with APIs, upload CSV data, or link to Google Sheets, and create customized prompts to extract specific data. The app utilizes the Groq and Scraper APIs to provide contextual responses, making data querying and retrieval seamless.

## Features

- **API Authentication**: Authenticate with Groq and Scraper APIs to enable advanced querying.
- **Data Input Options**: Upload a CSV file or link a Google Sheets document to input data.
- **Customizable Prompts**: Define custom prompts with placeholders for data columns to tailor queries for specific data points.
- **Data Retrieval & Export**: Generate outputs based on custom prompts, preview results, and download updated CSV files. For Google Sheets data, there’s an option to update the original sheet.

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/tonyStark-Jr/smart-query-ai.git
cd smart-query-ai
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the application using Streamlit:

```bash
streamlit run main_app.py
```

### Application Workflow

1. **Step 1: Authenticate with Groq API**  
   Enter your Groq API key to access the Groq API and authenticate it.

2. **Step 2: Authenticate with Scraper API**  
   Similarly, input your Scraper API key for web scraping capabilities.

3. **Step 3: Data Source Selection**  
   - **Upload CSV File**: Upload a CSV file to use as the data source.
   - **Google Sheets Link**: Upload JSON credentials for a Google service account and input the Google Sheets URL.

4. **Prompt Customization**  
   Define custom prompts with `{column_name}` placeholders to extract specific information. You can use multiple placeholders too. The app verifies column placeholders and generates output, which can be previewed and downloaded as a new CSV.

## File Descriptions

- **main_app.py**: The primary Streamlit application file. Manages the workflow of API authentication, data input, output display and user interaction.
- **scrap_search.py**: Handles prompt processing, generating outputs based on search results using the Scraper API.
- **utils.py**: Utility functions for Google Sheets interaction, API authentication, and fetching search results.

## Example Prompt Usage

To use the column data in your custom prompts, follow this format you can also use multiple placeholders:

```plaintext
Get me the email address of {company}.
```

## Contact

For any queries, reach out at [prakharshukla165@gmail.com](mailto:prakharshukla165@gmail.com).
