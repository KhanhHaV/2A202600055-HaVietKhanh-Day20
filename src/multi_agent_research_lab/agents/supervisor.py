"""Supervisor / router skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState


class SupervisorAgent(BaseAgent):
    """Decides which worker should run next and when to stop."""

    name = "supervisor"

    def run(self, state: ResearchState) -> ResearchState:
        """Update `state.route_history` with the next route."""
        from multi_agent_research_lab.core.config import get_settings
        
        settings = get_settings()
        if state.iteration >= settings.max_iterations:
            state.errors.append("Max iterations reached")
            state.record_route("done")
            return state
            
        if state.research_notes is None:
            state.record_route("researcher")
        elif state.analysis_notes is None:
            state.record_route("analyst")
        elif state.final_answer is None:
            state.record_route("writer")
        else:
            state.record_route("done")
            
        return state
