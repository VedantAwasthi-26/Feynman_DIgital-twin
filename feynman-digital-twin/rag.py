import chromadb

def get_collection():
    client = chromadb.PersistentClient(path="chroma_db")

    return client.get_collection(
        name="feynman_knowledge"
    )

def search_documents(query, n_results=3):
    collection = get_collection()

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results

def get_context(query):
    results = search_documents(query)

    documents = results["documents"][0]

    return "\n\n".join(documents)

if __name__ == "__main__":
    results = search_documents(
        "What is the atomic hypothesis?"
    )

    print(results["documents"][0][0][:500])

    print(get_context("What is the atomic hypothesis?")[:1000])