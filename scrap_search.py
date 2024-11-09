from utils import *
from groq import Groq

def getResponseFromSheet(custom_prompt,df,column_name):
    
    generated_prompts = [custom_prompt.replace(f"{{{column_name}}}", str(value)) for value in df[column_name]]
    
    web_search_results=[getSearchResults(prompt) for prompt in generated_prompts]
    
    final_model_prompts=[f"From the text given below {generated_prompts[i]}\n{web_search_results[i]}" for i in range(len(generated_prompts))]
    
    system_prompt="Give direct answer and keep it short and give only relevant answer and write nothing extra. If there are multiple answers return them seperated by a comma."
    
    generated_outputs=[getResponse(prompt,system_prompt=system_prompt) for prompt in final_model_prompts]
    
    return generated_outputs
    
