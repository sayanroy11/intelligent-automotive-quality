from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

from load_documents import load_documents,chunk_docs
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_PATH = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME='automotive_documents'

def build_vector_store():
    documents=load_documents()
    chunks=chunk_docs(documents)
    print(f'Loaded {len(documents)} documents')
    print(f'and {len(chunks)} chunks')
    model=SentenceTransformer('all-MiniLM-L6-v2')
    client=chromadb.PersistentClient(path=str(CHROMA_PATH))
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass;
    collection=client.create_collection(name=COLLECTION_NAME)
    texts=[chunk['text'] for chunk in chunks]
    embeddings=model.encode(texts).tolist()
    ids=[
        f'{chunk['source']}_{chunk['chunk_id']}'
        for chunk in chunks
    ]
    metadatas=[
        {
            "source":chunk['source'],
            "chunk_id":chunk['chunk_id']
        }
            for chunk in chunks
    ]
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )
    print(f'Stored {collection.count()} chunks in Chromadb')

if __name__=="__main__":
    build_vector_store()