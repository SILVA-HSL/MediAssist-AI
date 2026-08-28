import chromadb
from sentence_transformers import SentenceTransformer
from langchain_ollama import ChatOllama

#connect to the existing ChromaDB
chroma_client = chromadb.PersistentClient(
    path="../chroma_db"
)

collection = chroma_client.get_collection(
    name="hospital_documents"
)

#load embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

#connect to the Ollama model
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


#ask a question
question = input("\nAsk a hospital-related question: ")

#Convert question into embedding
query_embedding = embedding_model.encode(
    question
).tolist()


# Retrieve relevant documents
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

#Combine retrieved chunks
retrieved_documents = results["documents"][0]

context = "\n\n".join(
    retrieved_documents
)

#Create RAG prompt

prompt = f"""
You are a hospital information assistant.

Answer the user's question ONLY using the information
provided in the context below.

Do not use your own knowledge.

If the answer cannot be found in the context, respond:

"I could not find this information in the provided
hospital documents."

Context:
----------------
{context}
----------------

Question:
{question}

Answer:
"""

# Send prompt to Ollama
response = llm.invoke(prompt)

#display the response
print("\nResponse:")
print(response.content)