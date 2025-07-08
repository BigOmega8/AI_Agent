from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from documents.models import Document
from django.db.models import Q

@tool
def search_query_documents(query: str, limit:int=5, config:RunnableConfig = {}):
    """
    Search the most recent LIMIT documents for the current user  with maximum of 25.

    arguments:
    query: string or lookup search across title or content of document
    limit: number of results
    """
    # print(config)
    if limit > 25:
        limit = 25
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    default_lookups = {

        "active": True,
        
    }
    query_set = Document.objects.filter(**default_lookups).filter(
        Q(title__icontains=query) |
        Q(content__icontains=query)
    ).order_by("-created_at")
    response_data = []
    for data_obj in query_set[:limit]:
        response_data.append(
            {
                "id": data_obj.id,
                "title": data_obj.title
            }
        )
    return response_data

@tool
def list_documents(limit:int = 5, config:RunnableConfig= {}):
    """
    List the most recent LIMIT documents for the current user with maximum of 25.

    agruments
    limit: number of results
    """
    if limit > 25:
        limit = 25
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("error: User ID is required in the configuration.")
    query_set = Document.objects.filter(owner_id = user_id, active=True).order_by("-created_at")
    response_data = []

    for data_obj in query_set[:limit]:
        response_data.append(
            {
                "id": data_obj.id,
                "title": data_obj.title,
            }
        )
    
    return response_data

@tool
def get_document(document_id: int, config: RunnableConfig):
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
        "created_at": data_obj.created_at
    }

    return response_data

@tool
def create_document(title:str, content:str, config:RunnableConfig):
    """
    Create a new document to store for the user.

    Arguments are:
    title: string max characters of 120
    content: long form text in many paragraphs or pages
    """

    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("error: User ID is required in the configuration.")
    data_obj, created = Document.objects.get_or_create(
        title=title,
        content=content,
        owner_id=user_id,
        active=True
    )
    
    response_data = {
        "id": data_obj.id,
        "title": data_obj.title,
        "content": data_obj.content,
        "created_at": data_obj.created_at
    }

    return response_data

@tool
def update_document(document_id:int, title:str=None, content:str=None, config:RunnableConfig={}):
    """
    Create a new document to store for the user.

    Arguments are:
    document_id: int ID of the document to update
    title: string max characters of 120 (optional)
    content: long form text in many paragraphs or pages (optional)
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
        raise Exception("Invalid request!")
    
    if title is not None:
        data_obj.title = title
    if content is not None:
        data_obj.content = content
    if title or content:
        data_obj.save()
    
    response_data = {
        "id": data_obj.id,
        "title": data_obj.title,
        "content": data_obj.content,
        "created_at": data_obj.created_at
    }

    return response_data

@tool
def delete_document(document_id: int, config: RunnableConfig = {}):
    """
    Delete a document by its ID for the current user.
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
    data_obj.delete()  # Soft delete the document
    response_data = {"message": f"Document with ID {data_obj.id} deleted successfully."}

    return response_data

document_tools = [
    search_query_documents,
    create_document,
    list_documents,
    get_document,
    delete_document,
    update_document
]