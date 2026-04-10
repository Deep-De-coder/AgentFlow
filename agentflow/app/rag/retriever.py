from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores.supabase import SupabaseVectorStore
from supabase import create_client
from app.config import get_settings
from functools import lru_cache


@lru_cache
def get_vector_store() -> SupabaseVectorStore:
    s = get_settings()
    client = create_client(s.supabase_url, s.supabase_service_key)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=s.google_api_key,
    )
    return SupabaseVectorStore(
        client=client,
        embedding=embeddings,
        table_name="documents",
        query_name="match_documents",
    )


def retrieve(query: str, k: int = 4) -> list[dict]:
    store = get_vector_store()
    docs = store.similarity_search(query, k=k)
    return [
        {"content": d.page_content, "metadata": d.metadata}
        for d in docs
    ]
