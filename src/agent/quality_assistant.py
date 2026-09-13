import requests
from src.rag.retrieve import retrieve_documents
from src.knowledge_graph.query_graph import get_battery_overheating_stats
from src.agent.router import route_question

OLLAMA_URL='http://localhost:11434/api/generate'
MODEL_NAME='llama3.2:3b'

def build_graph_context():
    stats = get_battery_overheating_stats()
    lines = []

    for item in stats:
        line = (
            f"{item['supplier']}: "
            f"{item['overheating_cases']} overheating cases out of "
            f"{item['total_battery_inspections']} battery inspections "
            f"({item['overheating_rate']}% overheating rate)"
        )

        lines.append(line)

    graph_context = "\n".join(lines)
    return graph_context
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
    route=route_question(question)
    graph_context=""
    document_context=""
    rag_results=None
    if route in ['graph','hybrid']:
         graph_context = build_graph_context()
    if route in ['rag','hybrid']:
        rag_results=retrieve_documents(question,top_k=3)
        document_context=build_document_context(rag_results)
    prompt= f"""
You are an automotive quality investigation assistant.

Use only the evidence provided below.

Structured quality data from the knowledge graph:
{graph_context if graph_context else 'No structured data available'}

Technical documentation:
{document_context if document_context else 'No technical documentation available'}

Instructions:
- If structured quality data is provided, use its actual numbers directly.
- Compare suppliers using overheating rate, not only raw case count.
- Do not say that the data is unavailable if supplier statistics are provided above.
- Use the technical documentation only for recommended investigation steps.
- Do not invent facts.

Answer the user's question in two short sections:
1. Quality data findings
2. Recommended investigation

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
    return answer,route,rag_results

if __name__=='__main__':
    question=(
        'Is Supplier_B showing a battery overheating problem '
        'and what should engineers inspect?'
    )

    answer,route,rag_results=answer_quality_question(question)
    print('\nQuestion:')
    print(question)
    print('\nRoute:')
    print(route)
    print('\nAnswer:')
    print(answer)
    if rag_results:
        print('Retrieved document sources:')
        for metadata in rag_results['metadatas'][0]:
            print(f'-{metadata['source']}')