import requests
from retrieve import retrieve_documents

OOLAMA_URL="http://localhost:11434/api/generate"
MODEL_NAME="llama3.2:3b"

def build_context(results):
    documents=results['documents'][0]
    metadatas=results['metadatas'][0]
    context_parts=[]
    for document,metadata in zip(documents,metadatas):
        source=metadata['source']
        context_parts.append(
            f'Source: {source}\n{document}'
        )
    return "\n\n".join(context_parts)

def generate_answer(question):
    results=retrieve_documents(question,top_k=3)
    context=build_context(results)
    prompt=f"""
You are an automotive quality investigation assistant,

Answer the user's question using only the provided context.

If the answer is not supported by the context,say:
"I do not have enough information in the available documents."
Keep the answer concise and practical.

Context:
{context}

Question:
{question}

Answer:
"""
    response=requests.post(
        OOLAMA_URL,
        json={
            'model': MODEL_NAME,
            'prompt': prompt,
            'stream': False
        },
        timeout=120
    )
    response.raise_for_status()
    answer=response.json()['response']
    return answer,results

if __name__=='__main__':
    question='What should be checked when a battery is overheating'
    answer,results=generate_answer(question)
    print('\nQuestion:')
    print(question)
    print('\nAnswer:')
    print(answer)
    print('\nSources:')
    for metadata in results['metadatas'][0]:
        print(f'-{metadata['source']}')