from groq import Groq
import os
import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


default_system_prompt="Be a helpful assistant. Give short and direct answers. If you dont have answer just say that you dont have answer."
def get_google_sheet(url,json_cred):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_dict(json_cred, scope)
    client = gspread.authorize(creds)

    # Extract the sheet ID from the URL
    sheet_id = url.split('/')[5]

    # Open the spreadsheet
    sheet = client.open_by_key(sheet_id)

    # Get the first worksheet
    worksheet = sheet.sheet1

    # Convert the worksheet data to a Pandas DataFrame
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])

    return df

def update_google_sheet(url, df,json_cred):

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_dict(json_cred, scope)

    client = gspread.authorize(creds)

    # Extract the sheet ID from the URL
    sheet_id = url.split('/')[5]

    # Open the spreadsheet
    sheet = client.open_by_key(sheet_id)

    # Get the first worksheet
    worksheet = sheet.sheet1

    # Clear the existing data
    # current_values = worksheet.get_all_values()

    worksheet.clear()
    # worksheet.update(current_values[:1] + df.values.tolist())

    # # Update the worksheet with the new data
    worksheet.update([df.columns.tolist()]+df.values.tolist())

def getSearchResults(query):
    payload={
        'api_key':os.environ['SCRAPER_API_KEY'],
        'country':'in',
        'query':query
    }
    r = requests.get('https://api.scraperapi.com/structured/google/search', params=payload)
    data=json.loads(r.text)
    return data["organic_results"]

def authenticate_scraper_api():
    try:
        r = requests.get('https://api.scraperapi.com/structured/google/search')
        return 1
    except Exception as e:
        print(e)
        return 0
    
def authenticate_groq_api():
    try:
        client = Groq(
            api_key=os.environ['GROQ_API_KEY'],
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Hello LLM!",
                }
            ],
            model="llama3-8b-8192",
        )
        return 1
    except Exception as e:
        print(e)
        return 0


def getResponse(prompt,model='llama3-8b-8192',system_prompt=default_system_prompt): 
    client = Groq(
        api_key=os.environ['GROQ_API_KEY'],
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                
                "role": "system",
                "content": system_prompt,
            
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )

    return (chat_completion.choices[0].message.content)