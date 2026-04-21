from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
import os
import shutil
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from embeddings import get_embedding_function
from rag_pipeline import run_autopsy
from seed_data import ingest_baseline_data

def validate_and_correct_score(result: dict) -> dict:
    """
    Prevents LLM from always returning 85.
    Recalculates death score from failureDNA if LLM output seems biased.
    """
    dna = result.get("failureDNA", [])
    
    if not dna:
        return result
    
    # Calculate weighted severity score from DNA factors
    # Each factor contributes: weight * severity_multiplier
    severity_keywords_high = [
        "fatal", "certain", "impossible", "fraud", 
        "bankrupt", "proven", "guaranteed"
    ]
    severity_keywords_low = [
        "possible", "minor", "manageable", 
        "addressable", "common", "typical"
    ]
    
    weighted_score = 0
    total_weight = 0
    
    for factor in dna:
        weight = factor.get("weight", 25)
        detail = factor.get("detail", "").lower()
        
        # Determine severity from language used
        if any(word in detail for word in severity_keywords_high):
            severity = 0.95
        elif any(word in detail for word in severity_keywords_low):
            severity = 0.5
        else:
            severity = 0.72  # neutral default
        
        weighted_score += weight * severity
        total_weight += weight
    
    if total_weight > 0:
        calculated_score = int(weighted_score / total_weight * 100)
    else:
        calculated_score = result.get("deathScore", 70)
    
    llm_score = result.get("deathScore", 70)
    
    # If LLM score is suspiciously between 80-90 (bias zone),
    # blend it with calculated score
    if 80 <= llm_score <= 90:
        final_score = int((llm_score * 0.4) + (calculated_score * 0.6))
    else:
        final_score = llm_score
    
    # Hard clamp — nothing above 95 unless truly catastrophic
    final_score = max(10, min(95, final_score))
    
    result["deathScore"] = final_score
    return result

@asynccontextmanager
async def lifespan(app):
    # Auto-seed ChromaDB on startup
    ingest_baseline_data()
    yield

app = FastAPI(title="Corporate Autopsy API", lifespan=lifespan)

# Add CORS Middleware
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:5174,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AutopsyRequest(BaseModel):
    idea: str

def get_vectorstore():
    return Chroma(
        collection_name=os.getenv("COLLECTION_NAME", "startup_failures"),
        persist_directory=os.getenv("CHROMA_PATH", "./chroma_db"),
        embedding_function=get_embedding_function()
    )

@app.get("/")
def read_root():
    vs = get_vectorstore()
    count = vs._collection.count()
    return {"status": "online", "docs_indexed": count}

@app.get("/health")
def read_health():
    vs = get_vectorstore()
    count = vs._collection.count()
    provider = os.getenv("LLM_PROVIDER", "groq")
    return {"status": "ok", "vector_docs": count, "llm_provider": provider}

@app.post("/autopsy")
async def process_autopsy(req: AutopsyRequest):
    if not req.idea or len(req.idea.strip()) == 0:
        raise HTTPException(status_code=400, detail="Idea cannot be empty")
    
    result = await run_autopsy(req.idea)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    
    result = validate_and_correct_score(result)
    return result

@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    tmp_path = f"/tmp/{file.filename}"
    # On Windows /tmp/ might not exist reliably, use OS temp directory, or local directory
    tmp_path = os.path.join(".", file.filename)
    
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        if file.filename.endswith(".pdf"):
            loader = PyPDFLoader(tmp_path)
        else:
            loader = TextLoader(tmp_path)
            
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        chunks = splitter.split_documents(docs)
        
        vs = get_vectorstore()
        vs.add_documents(chunks)
        os.remove(tmp_path)
        
        return {"status": "ingested", "chunks_added": len(chunks)}
    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/graveyard/search")
def graveyard_search(query: str, limit: int = 5):
    vs = get_vectorstore()
    docs = vs.similarity_search(query, k=limit)
    results = [{"content": d.page_content, "metadata": d.metadata} for d in docs]
    return {"results": results}
