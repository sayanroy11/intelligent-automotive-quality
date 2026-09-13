from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from src.agent.quality_assistant import answer_quality_question
#127.0.0.1:8000/docs
#uvicorn src.api.main:app --reload
app=FastAPI(
    title='Automotive Quality Intelligence API',
    description=(
        'API for investigating automotive quality issues '
        'using a Knowledge graph, RAG and local LLM'
    ),
    version='1.0.0'
)

class QuestionRequest(BaseModel):
    question:str
@app.get('/')
def root():
    return{
        'message':'Automotive quality intelligence API is running'
    }

@app.get('/health')
def health():
    return{
        'status':'Healthy'
    }
@app.post('/ask')
def ask_question(request:QuestionRequest):
    try:
         answer,route,rag_results=answer_quality_question(request.question)
         sources=[]
         if rag_results:
             for metadata in rag_results['metadatas'][0]:
                 source=metadata['source']
                 if source not in sources:
                     sources.append(source)
         return{
            'question':request.question,
            'route':route,
            'answer':answer,
            'sources':sources
        }
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )