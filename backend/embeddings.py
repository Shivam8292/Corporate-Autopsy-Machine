import os

def get_embedding_function():
    """Returns the appropriate embedding function based on environment."""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )
    else:
        # Fallback to local embeddings (requires sentence-transformers)
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name=os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
        )
