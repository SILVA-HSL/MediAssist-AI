import chromadb
from sentence_transformers import SentenceTransformer
from langchain_core.tools import tool

#Connect to ChromaDB
chroma_client = chromadb.PersistentClient(
    path="../chroma_db"
)

collection = chroma_client.get_collection(
    name="hospital_documents"
)

# Load embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# RAG search tool
# @tool
# def search_hospital_documents(query: str):
#     """
#     Search the hospital's internal documents for information
#     related to the user's question. Use this tool for policies,
#     procedures, services, guidelines, facilities, and other
#     information contained in hospital documents.
#     """

#     query_embedding = embedding_model.encode(
#         query
#     ).tolist()

#     results = collection.query(
#         query_embeddings=[query_embedding],
#         n_results=3
#     )

#     retrieved_documents = results["documents"][0]

#     if not retrieved_documents:
#         return "No relevant information was found in the hospital documents."

#     context = "\n\n".join(
#         retrieved_documents
#     )

#     return context

#========================================================
@tool
def search_hospital_documents(query: str):
    """
    Search the hospital's internal documents for information
    related to the user's question. Use this tool for policies,
    procedures, services, guidelines, facilities, and other
    information contained in hospital documents.
    """

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    retrieved_documents = results["documents"][0]
    retrieved_metadatas = results["metadatas"][0]

    if not retrieved_documents:
        return {
            "context": "No relevant information was found in the hospital documents.",
            "sources": []
        }

    context = "\n\n".join(
        retrieved_documents
    )

    sources = list({
        metadata.get("source")
        for metadata in retrieved_metadatas
        if metadata.get("source")
    })

    return {
        "context": context,
        "sources": sources
    }