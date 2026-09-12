import requests
from src.rag.retrieve import retrieve_documents
from src.knowledge_graph.query_graph import get_battery_overheating_stats

OLLAMA_URL='http://localhost:11434/api/generate'
MODEL_NAME='llama3.2:3b'

def build_graph_context():
    stats=get_battery_overheating_stats()
    lines=[]
    for item in stats:
        lines.append(
            f'{item['supplier']}:'
            f'{item['overheating_cases']} overheating cases out of '
            f'{item['total_battery_inspections']} battery inspections '
            f'{item['overheating_rate']} % overheating rate '
        )
    return "\n".join(lines)

def build_document_context(results):
    documents=results['documents'][0]
    metadatas=results['metadatas'][0]

    context_parts=[]

    for document,metadata in zip(documents,metadatas):
        context_parts.append(
            f'Source: {metadata['source']}\n{document}'
        )
    return '\n\n'.join(context_parts)

def answer_quality_question(question):
    graph_context=build_graph_context()
    rag_results=retrieve_documents(question,top_k=3)
    document_context=build_document_context(rag_results)
    prompt= f"""
You are an automotive quality investigation assistant.

Use only the evidence provided below.

Structured quality data from the knowledge graph:
{graph_context}

Technical documentation:
{document_context}

Answer the user's question using both sources when relevant.
Clearly distinguish:
1. What the quality data shows.
2. What engineers should investigate.

Do not invent causes that are not supported by the provided evidence.
 
Question:
{question}
Answer:
"""
    response=requests.post(
        OLLAMA_URL,
        json={
            'model':MODEL_NAME,
            'prompt':prompt,
            'stream':False
        },
        timeout=120
    )

    response.raise_for_status()
    answer=response.json()['response']
    return answer,rag_results

if __name__=='__main__':
    question=(
        'Is Supplier_B showing a battery overheating problem '
        'and what should engineers inspect?'
    )

    answer,rag_results=answer_quality_question(question)
    print('\nQuestion:')
    print(question)
    print('\nAnswer:')
    print(answer)
    print('Retrieved document sources:')
    for metadata in rag_results['metadatas'][0]:
        print(f'-{metadata['source']}')