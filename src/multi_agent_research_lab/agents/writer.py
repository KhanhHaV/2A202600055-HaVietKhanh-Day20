"""Writer agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState


class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.final_answer`."""
        from multi_agent_research_lab.core.schemas import AgentName, AgentResult
        from multi_agent_research_lab.services.llm_client import LLMClient
        
        system_prompt = f"You are an expert technical writer. Write a comprehensive response to the user's query tailored to {state.request.audience}. Use the provided research and analysis notes. Include citations or source references where appropriate."
        user_prompt = f"Query: {state.request.query}\n\nResearch Notes:\n{state.research_notes}\n\nAnalysis Notes:\n{state.analysis_notes}"
        
        llm = LLMClient()
        response = llm.complete(system_prompt, user_prompt)
        
        state.final_answer = response.content
        state.agent_results.append(AgentResult(
            agent=AgentName.WRITER,
            content=response.content,
            metadata={"input_tokens": response.input_tokens, "output_tokens": response.output_tokens, "cost_usd": response.cost_usd}
        ))
        
        return state
