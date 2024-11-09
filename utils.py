from groq import Groq
import os
import requests
import json


default_system_prompt="Be a helpful assistant. Give short and direct answers. If you dont have answer just say that you dont have answer."

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
        api_key="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",
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