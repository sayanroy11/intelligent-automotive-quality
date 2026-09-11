from sentence_transformers import SentenceTransformer
import chromadb

CHROMA_PATH="chroma_db"
COLLECTION_NAME='automotive_documents'
def retrieve_documents(query,top_k=3):
    model=SentenceTransformer('all-MiniLM-L6-v2')
    client=chromadb.PersistentClient(path=CHROMA_PATH)
    collection=client.get_collection(name=COLLECTION_NAME)
    query_embedding=model.encode_query(query).tolist()
    results=collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results
if __name__=='__main__':
    question='what should be checked when a battery is overheating?'
    results=retrieve_documents(question)
    print(f'\nQuestion: {question}')
    for index,document in enumerate(results['documents'][0],start=1):
        print('\n---')
        print(f'Result {index}')
        print(f'Source: {results['metadatas'][0][index-1]['source']}')
        print(document)