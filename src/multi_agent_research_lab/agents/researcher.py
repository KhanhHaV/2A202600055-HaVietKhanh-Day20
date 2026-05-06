"""Researcher agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState


class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""

    name = "researcher"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.sources` and `state.research_notes`."""

        from multi_agent_research_lab.core.schemas import AgentName, AgentResult
        from multi_agent_research_lab.services.llm_client import LLMClient
        from multi_agent_research_lab.services.search_client import SearchClient
        
        search_client = SearchClient()
        sources = search_client.search(state.request.query, max_results=state.request.max_sources)
        state.sources.extend(sources)
        
        sources_text = "\n\n".join([f"Title: {s.title}\nURL: {s.url}\nSnippet: {s.snippet}" for s in sources])
        
        system_prompt = "You are a professional researcher. Summarize the following sources to answer the user query. Provide a concise summary of the factual information found."
        user_prompt = f"Query: {state.request.query}\n\nSources:\n{sources_text}"
        
        llm = LLMClient()
        response = llm.complete(system_prompt, user_prompt)
        
        state.research_notes = response.content
        state.agent_results.append(AgentResult(
            agent=AgentName.RESEARCHER,
            content=response.content,
            metadata={"input_tokens": response.input_tokens, "output_tokens": response.output_tokens, "cost_usd": response.cost_usd}
        ))
        
        return state
