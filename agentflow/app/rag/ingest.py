"""
Run once to populate Supabase with sample docs:
  python -m app.rag.ingest
"""
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores.supabase import SupabaseVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from supabase import create_client
from app.config import get_settings
from docs.sample_docs import SAMPLE_DOCUMENTS


def ingest():
    s = get_settings()
    client = create_client(s.supabase_url, s.supabase_service_key)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=s.google_api_key,
    )
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    docs = [
        Document(page_content=d["content"], metadata=d["metadata"])
        for d in SAMPLE_DOCUMENTS
    ]
    chunks = splitter.split_documents(docs)
    SupabaseVectorStore.from_documents(
        chunks,
        embeddings,
        client=client,
        table_name="documents",
        query_name="match_documents",
    )
    print(f"Ingested {len(chunks)} chunks into Supabase.")


if __name__ == "__main__":
    ingest()
