import chromadb
from sentence_transformers import SentenceTransformer

#Connect to existing ChromaDB
chroma_client = chromadb.PersistentClient(
    path="../chroma_db"
)

#Get existing collection
collection = chroma_client.get_collection(
    name="hospital_documents"
)

#Load the SAME embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Ask a question
query = "What should healthcare staff do if a patient has a drug allergy?"
# query = "What should be checked before giving medication?"
# query = "How should critical patients be handled?"

# Convert question into embedding
query_embedding = embedding_model.encode(
    query
).tolist()

#search chromadb collection for relevant documents
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

#Print the results
print("\nQuestion:")
print(query)

print("\nRetrieved Documents:\n")

for document, metadata in zip(
    results["documents"][0],
    results["metadatas"][0]
):
    print("Source:", metadata["source"])
    print("Content:", document)
    print("-" * 50)