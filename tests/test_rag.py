import pytest
from unittest.mock import patch, MagicMock


def test_retrieve_returns_list():
    mock_docs = [
        MagicMock(
            page_content="Cloud Run is serverless.",
            metadata={"source": "gcp_cloud_run"}
        )
    ]
    with patch("app.rag.retriever.get_vector_store") as mock_store:
        mock_store.return_value.similarity_search.return_value = mock_docs
        from app.rag.retriever import retrieve
        results = retrieve("Cloud Run")
        assert isinstance(results, list)
        assert len(results) == 1
        assert "content" in results[0]
        assert "metadata" in results[0]


def test_retrieve_empty_returns_empty_list():
    with patch("app.rag.retriever.get_vector_store") as mock_store:
        mock_store.return_value.similarity_search.return_value = []
        from app.rag.retriever import retrieve
        results = retrieve("something obscure")
        assert results == []
