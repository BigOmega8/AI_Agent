from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from documents.models import Document

@tool
def list_documents(config: RunnableConfig = None):
    """
    List the most recent 5 documents for the current user.
    """
    
    limit = 5
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("error: User ID is required in the configuration.")
    query_set = Document.objects.filter(owner_id = user_id, active=True).order_by("-created_at")
    response_data = []

    for doc in query_set[:limit]:
        response_data.append(
            {
                "id": doc.id,
                "title": doc.title,
                "content": doc.content,
                "active": doc.active,
                "active_at": doc.active_at,
                "created_at": doc.created_at,
                "updated_at": doc.updated_at
            }
        )
    
    return response_data

@tool
def get_document(document_id: int, config: RunnableConfig = None):
    """
    Get a document by its ID for a given user.
    """

    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("error: User ID is required in the configuration.")
    try:
        data_obj = Document.objects.get(id=document_id, owner_id=user_id, active=True)
    except Document.DoesNotExist:
        raise Exception("error: Document not found or inactive.")
    except:
        raise  Exception("Invalid request!")
    response_data = {
        "id": data_obj.id,
        "title": data_obj.title,
        "content": data_obj.content,
        "active": data_obj.active,
        "active_at": data_obj.active_at,
        "created_at": data_obj.created_at,
        "updated_at": data_obj.updated_at
    }

    return response_data

document_tools = [
    list_documents,
    get_document
]