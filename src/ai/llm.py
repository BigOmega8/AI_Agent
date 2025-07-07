from langchain_openai import ChatOpenAI
from django.conf import settings

def get_openai_model(model="gpt-4o-mini"):
    """
    Returns the OpenAI model based on the provided model name.
    """
    
    return ChatOpenAI(
        model=model,
        temperature=2,
        max_retries=2,
        api_key=settings.OPENAI_API_KEY  # Set your OpenAI API key here
    )