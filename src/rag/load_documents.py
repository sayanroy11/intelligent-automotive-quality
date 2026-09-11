from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
DOCS_PATH=Path(__file__).resolve().parents[2]/'docs'

def load_documents():
    docs=[]
    for file in DOCS_PATH.glob("*.md"):
        text=file.read_text(encoding="utf-8")
        docs.append({
            "source":file.name,
            "text":text
        })
    return docs

def chunk_docs(documents):
    splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100)
    chunks=[]
    for document in documents:
        split_texts=splitter.split_text(document['text'])
        for index,chunk in enumerate(split_texts):
            chunks.append({
                "source": document["source"],
                "chunk_id": index,
                "text": chunk
            })
    return chunks
if __name__ == "__main__":
    documents=load_documents()
    chunks=chunk_docs(documents)

    print(f'Loaded documents: {len(documents)}')
    print(f'Created chunks {len(chunks)}')
    for chunk in chunks:
        print('\n---')
        print(f'Source: {chunk['source']}')
        print(chunk['text'])