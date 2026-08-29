import chromadb


chroma_client = chromadb.PersistentClient(
    path="../chroma_db"
)

collection = chroma_client.get_collection(
    name="hospital_documents"
)

print("Collection:", collection.name)
print("Number of documents:", collection.count())

results = collection.get(
    include=["documents", "metadatas"]
)

print("\n==============================")
print("STORED DOCUMENTS")
print("==============================")

for i, document in enumerate(results["documents"]):

    print(f"\n--- Chunk {i + 1} ---")
    print(document)

    if results["metadatas"]:
        print("Metadata:", results["metadatas"][i])