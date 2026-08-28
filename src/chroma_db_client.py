import chromadb
from sentence_transformers import SentenceTransformer
import os


chroma_client = chromadb.PersistentClient(
    path="../chroma_db"
)



#create chromadb collection
collection = chroma_client.get_or_create_collection(name="hospital_documents")


#load the sentence transformer model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

#read documents
documents_folder = "../documents"

documents = []

for filename in os.listdir(documents_folder):

    if filename.endswith(".txt"):

        file_path = os.path.join(
            documents_folder,
            filename
        )

        with open(file_path, "r", encoding="utf-8") as file:

            content = file.read()

            documents.append({
                "filename": filename,
                "content": content
            })

#Simple chunking function


def chunk_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i + chunk_size]

        chunks.append(chunk)

    return chunks

#Process each document
document_chunks = []
document_ids = []
document_metadata = []


for document in documents:

    chunks = chunk_text(document["content"])

    for index, chunk in enumerate(chunks):

        document_chunks.append(chunk)

        document_ids.append(
            f"{document['filename']}_chunk_{index}"
        )

        document_metadata.append({
            "source": document["filename"]
        })

# Generate embeddings
embeddings = embedding_model.encode(
    document_chunks
).tolist()


#add to chroma collection
collection.add(
    ids=document_ids,
    documents=document_chunks,
    embeddings=embeddings,
    metadatas=document_metadata
)
print("Documents successfully stored in ChromaDB!")

print(f"Total chunks stored: {len(document_chunks)}")