import os
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

def ingest_scraped_data():
    try:
        print("Starting ingestion for scraped failure data...")
        with open("scraped_failures.json", "r") as f:
            data = json.load(f)

        vectorstore = Chroma(
            collection_name=os.getenv("COLLECTION_NAME", "startup_failures"),
            persist_directory=os.getenv("CHROMA_PATH", "./chroma_db"),
            embedding_function=HuggingFaceEmbeddings(
                model_name=os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
            )
        )
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        docs = []

        for item in data:
            chunks = splitter.split_text(item["description"])
            for chunk in chunks:
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "company": item["company"],
                        "source": "cb_insights_postmortem"
                    }
                )
                docs.append(doc)
        
        vectorstore.add_documents(docs)
        print(f"Ingestion complete. Added {len(docs)} scraped chunks to ChromaDB.")
        
        count = vectorstore._collection.count()
        print(f"Total documents in collection: {count}")
    except Exception as e:
        print(f"Error during ingestion: {e}")

if __name__ == "__main__":
    ingest_scraped_data()
