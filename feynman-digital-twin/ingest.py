import os
from sentence_transformers import SentenceTransformer
import chromadb

def get_chroma_collection():
    client = chromadb.PersistentClient(path="chroma_db")

    collection = client.get_or_create_collection(
        name="feynman_knowledge"
    )

    return collection

def load_text_files(data_folder="data"):
    documents = []

    for root, _, files in os.walk(data_folder):
        for file in files:
            if file.endswith(".txt"):
                path = os.path.join(root, file)

                with open(path, "r", encoding="utf-8") as f:
                    documents.append(
                        {
                            "file": file,
                            "content": f.read()
                        }
                    )

    return documents

def chunk_documents(documents, chunk_size=1000):
    chunks = []

    for doc in documents:
        text = doc["content"]

        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]

            chunks.append(
                {
                    "source": doc["file"],
                    "content": chunk
                }
            )

    return chunks

def create_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def store_chunks(collection, chunks, embedding_model):
    for i, chunk in enumerate(chunks):
        embedding = embedding_model.encode(
            chunk["content"]
        ).tolist()

        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[chunk["content"]],
            metadatas=[
                {
                    "source": chunk["source"]
                }
            ]
        )

collection = get_chroma_collection()

print("Collection created successfully!")


documents = load_text_files()

print(f"Loaded {len(documents)} documents")


chunks = chunk_documents(documents)

print(f"Created {len(chunks)} chunks")

embedding_model = create_embedding_model()

print("Embedding model loaded!")

store_chunks(
    collection,
    chunks,
    embedding_model
)

print("Chunks stored successfully!")