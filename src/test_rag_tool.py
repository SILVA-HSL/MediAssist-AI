from tools.rag_tools import search_hospital_documents


result = search_hospital_documents.invoke({
    "query": "What are the hospital visiting hours?"
})

print("\nRetrieved Context:")
print(result)