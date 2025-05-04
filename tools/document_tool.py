from langchain.tools import Tool
from utils.vector_utils import get_vectorstore

def document_search_tool():
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})
    return Tool.from_function(
        func=lambda q: retriever.get_relevant_documents(q),
        name="Document Retriever",
        description="Search user-uploaded documents for personalized agricultural info."
    )
