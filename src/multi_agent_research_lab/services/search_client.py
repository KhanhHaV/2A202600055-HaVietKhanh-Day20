"""Search client abstraction for ResearcherAgent."""

from multi_agent_research_lab.core.schemas import SourceDocument


class SearchClient:
    """Provider-agnostic search client skeleton."""

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Search for documents relevant to a query.
        
        Using a mock since TAVILY_API_KEY is not strictly required.
        """
        return [
            SourceDocument(
                title="GraphRAG Overview",
                url="https://example.com/graphrag",
                snippet="GraphRAG combines knowledge graphs with large language models to provide more accurate and context-aware responses compared to standard RAG. It extracts entities and relationships to build a graph.",
                metadata={"source": "mock"}
            ),
            SourceDocument(
                title="State of the Art in Multi-Agent Systems",
                url="https://example.com/multi-agent",
                snippet="Recent advancements in multi-agent research emphasize the importance of distinct roles like Researcher, Analyst, and Writer to minimize hallucinations and improve answer quality. LangGraph is a popular framework for this.",
                metadata={"source": "mock"}
            )
        ][:max_results]
