"""Analyst agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState


class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.analysis_notes`."""
        from multi_agent_research_lab.core.schemas import AgentName, AgentResult
        from multi_agent_research_lab.services.llm_client import LLMClient
        
        system_prompt = "You are an analytical agent. Extract key claims, compare viewpoints, and identify any missing or weak evidence from the provided research notes."
        user_prompt = f"Query: {state.request.query}\n\nResearch Notes:\n{state.research_notes}"
        
        llm = LLMClient()
        response = llm.complete(system_prompt, user_prompt)
        
        state.analysis_notes = response.content
        state.agent_results.append(AgentResult(
            agent=AgentName.ANALYST,
            content=response.content,
            metadata={"input_tokens": response.input_tokens, "output_tokens": response.output_tokens, "cost_usd": response.cost_usd}
        ))
        
        return state
