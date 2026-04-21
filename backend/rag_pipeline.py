import os
import json
from langchain_chroma import Chroma
from embeddings import get_embedding_function
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Ollama
from dotenv import load_dotenv

load_dotenv()

PROMPT_TEMPLATE = """You are the Corporate Autopsy Machine, trained on hundreds of real startup failure post-mortems. Your job is to produce a structured failure analysis.

FAILURE DATABASE \u2014 RETRIEVED EVIDENCE:
{context}

STARTUP IDEA SUBMITTED FOR AUTOPSY:
{idea}

BEFORE scoring, consider these questions honestly:
1. Does a proven market already exist for this idea?
2. Are there successful companies doing something similar today?
3. Is the timing good (2024-2025 context)?
4. Does the founder have an obvious unfair advantage?

If answers to 3 or more are YES → score should be below 55
If answers to 2 are YES → score should be below 70
If answers to 0-1 are YES → score can be 70+

You are a balanced analyst, not a pessimist.
Your job is ACCURACY, not drama.

DEATH SCORE CALIBRATION — You MUST follow this scale strictly:

0-20  → Strong idea. Proven market exists. Clear demand. 
         Low competition or strong differentiation.
         Example: A fintech tool in 2010, early food delivery apps.

21-40 → Decent idea. Market exists but execution will be hard.
         Some competition but survivable. Needs good timing.
         Example: A niche SaaS for a specific industry.

41-60 → Risky idea. At least 1-2 serious red flags.
         Similar companies have struggled but some survived.
         Market is crowded or unit economics are unclear.

61-80 → Dangerous idea. 3+ structural problems visible.
         Multiple companies have failed with this exact model.
         Needs major pivot to survive.

81-100 → Near-certain death. 4+ fatal flaws.
          ONLY give this if the idea is nearly identical to a 
          company in the failure database AND has no differentiation.
          Example: Building Juicero again in 2025.

STRICT RULES FOR SCORING:
- Most ideas should score between 40-70
- Only give 80+ if idea directly mirrors a failed company with zero differentiation
- Only give below 30 if idea has clear market validation and no structural problems matching the failure database
- deathScore MUST equal the weighted average of failureDNA weights multiplied by each factor's severity (1.0 = certain, 0.5 = possible)
- If your highest failureDNA weight is 40% and severity is moderate, deathScore cannot exceed 65

Based ONLY on the failure patterns in the evidence above, respond with a single valid JSON object. No markdown. No explanation. Just JSON.

{{
  "deathScore": <integer 0-100, probability of failure>,
  "causeOfDeath": "<3-6 word dramatic cause of death>",
  "similarFailures": [
    {{"name": "<company from evidence>", "year": <int>, "similarity": <0-100>, "reason": "<specific pattern match>"}},
    {{"name": "...", "year": ..., "similarity": ..., "reason": "..."}},
    {{"name": "...", "year": ..., "similarity": ..., "reason": "..."}}
  ],
  "failureDNA": [
    {{"factor": "<factor name>", "weight": <int>, "detail": "<one sentence with data>"}},
    {{"factor": "...", "weight": ..., "detail": "..."}},
    {{"factor": "...", "weight": ..., "detail": "..."}},
    {{"factor": "...", "weight": ..., "detail": "..."}}
  ],
  "pivots": [
    "<specific actionable pivot 1>",
    "<specific actionable pivot 2>",
    "<specific actionable pivot 3>"
  ],
  "verdict": "<2-3 sentence brutally honest coroner verdict with real numbers>"
}}

RULES:
- failureDNA weights must sum to exactly 100
- similarFailures must reference companies from the evidence context
- verdict must include at least one real dollar figure or percentage
- deathScore above 80 means near-certain failure
"""

async def run_autopsy(idea: str) -> dict:
    try:
        # 1. Load vector store
        vectorstore = Chroma(
            collection_name=os.getenv("COLLECTION_NAME", "startup_failures"),
            persist_directory=os.getenv("CHROMA_PATH", "./chroma_db"),
            embedding_function=get_embedding_function()
        )

        # 2. Retrieve chunks (MMR)
        docs = vectorstore.max_marginal_relevance_search(
            query=idea,
            k=8,
            fetch_k=20,
            lambda_mult=0.5
        )

        # 3. Build context
        context_parts = []
        sources = set()
        for i, doc in enumerate(docs):
            source = doc.metadata.get('source', f'source_{i}')
            sources.add(source)
            context_parts.append(f"[SOURCE: {source}]\n{doc.page_content}\n")
        
        context_str = "\n".join(context_parts)

        # 4. Build Prompt
        prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["context", "idea"]
        )
        formatted_prompt = prompt.format(context=context_str, idea=idea)

        # 5. Initialize LLM
        provider = os.getenv("LLM_PROVIDER", "groq").lower()
        if provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                return {"error": "GROQ_API_KEY is virtually empty in .env. Please configure it."}
            llm = ChatGroq(
                groq_api_key=api_key,
                model_name=os.getenv("GROQ_MODEL", "mixtral-8x7b-32768"),
                temperature=0.1
            )
        elif provider == "google":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                return {"error": "GEMINI_API_KEY is missing in .env."}
            llm = ChatGoogleGenerativeAI(
                model="gemini-flash-lite-latest",
                google_api_key=api_key,
                temperature=0.1
            )
        else:
            llm = Ollama(
                model=os.getenv("OLLAMA_MODEL", "mistral"),
                temperature=0.1
            )

        # 6. Invoke LLM and strip json fences
        response = llm.invoke(formatted_prompt)
        if hasattr(response, "content"):
            text_response = response.content
        else:
            text_response = str(response)
        
        # Handle cases where content might be a list (e.g. multi-part)
        if isinstance(text_response, list):
            text_response = "".join([str(part.get("text", "") if hasattr(part, "get") else part) for part in text_response])
        
        text_response = text_response.strip()
        if text_response.startswith("```json"):
            text_response = text_response[7:]
        if text_response.startswith("```"):
            text_response = text_response[3:]
        if text_response.endswith("```"):
            text_response = text_response[:-3]
        
        # 7. Parse JSON and attach sources
        result = json.loads(text_response.strip())
        result["sources"] = list(sources)
        return result

    except json.JSONDecodeError as jde:
        return {
            "error": "LLM failed to produce valid JSON data structure.",
            "raw_output": text_response
        }
    except Exception as e:
        return {"error": str(e)}
