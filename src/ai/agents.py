from langgraph.prebuilt import create_react_agent
from ai.llm import get_openai_model
from ai.tools import document_tools

def get_document_agent(model=None, checkpointer=None):
    """
    Create and return a React agent with the specified tools.
    """
    
    llm_model = get_openai_model(model=model)
    agent = create_react_agent(
        model = llm_model,
        tools = document_tools,
        prompt = "You are a helpful assistant that can interact with documents. Use the tools provided to answer questions about documents.",
        checkpointer=checkpointer
    )

    return agent