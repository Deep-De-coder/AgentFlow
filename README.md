# AgentFlow

LangGraph ReAct agent with RAG + web search, deployed on GCP Cloud Run.

## Stack
- **LLM:** Gemini 1.5 Flash (free tier)
- **Orchestration:** LangGraph ReAct pattern
- **RAG:** Supabase pgvector (free tier)
- **Tracing:** Langfuse (free tier)
- **Deploy:** GCP Cloud Run (free tier)

## Local Setup

1. Clone and install:
   ```
   pip install -r requirements.txt
   ```

2. Copy and fill env vars:
   ```
   cp .env.example .env
   ```

3. Set up Supabase — run this SQL in your Supabase project:
   ```sql
   create extension if not exists vector;
   create table documents (
     id bigserial primary key,
     content text,
     metadata jsonb,
     embedding vector(768)
   );
   create or replace function match_documents(
     query_embedding vector(768),
     match_count int default 4
   )
   returns table (
     id bigint,
     content text,
     metadata jsonb,
     similarity float
   )
   language plpgsql
   as $$
   begin
     return query
     select id, content, metadata,
       1 - (documents.embedding <=> query_embedding) as similarity
     from documents
     order by documents.embedding <=> query_embedding
     limit match_count;
   end;
   $$;
   ```

4. Ingest sample docs:
   ```
   python -m app.rag.ingest
   ```

5. Run locally:
   ```
   uvicorn app.main:app --reload --port 8080
   ```

6. Test:
   ```
   curl -X POST http://localhost:8080/query \
     -H "Content-Type: application/json" \
     -d '{"query": "What is LangGraph?"}'
   ```

## Deploy to Cloud Run

Add these GitHub secrets:
- `GCP_SA_KEY` — GCP service account JSON key
- `GCP_PROJECT_ID` — your GCP project ID

Push to main — GitHub Actions runs Cloud Build and deploys.

## Tracing

Every agent run creates a trace in Langfuse.
View at: https://cloud.langfuse.com
