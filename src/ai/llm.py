from langchain_openai import ChatOpenAI
from django.conf import settings

def get_openai_api_key():
    """
    Returns the OpenAI API key from the settings.
    """
    
    if not settings.OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not set in the settings.")
    
    return settings.OPENAI_API_KEY

def get_openai_model(model="gpt-4o"):
    """
    Returns the OpenAI model based on the provided model name.
    """
    
    if model is None:
        model = "gpt-4o-mini"
        
    return ChatOpenAI(
        model=model,
        temperature=0,
        max_retries=2,
        api_key=get_openai_api_key(), 
    )