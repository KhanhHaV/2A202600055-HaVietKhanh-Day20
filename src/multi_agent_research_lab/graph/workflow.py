"""LangGraph workflow skeleton."""

from typing import Any

from multi_agent_research_lab.core.state import ResearchState


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph.

    Keep orchestration here; keep agent internals in `agents/`.
    """

    def build(self) -> Any:
        """Create a LangGraph graph."""
        from langgraph.graph import END, StateGraph

        from multi_agent_research_lab.agents.analyst import AnalystAgent
        from multi_agent_research_lab.agents.researcher import ResearcherAgent
        from multi_agent_research_lab.agents.supervisor import SupervisorAgent
        from multi_agent_research_lab.agents.writer import WriterAgent
        
        # Initialize agents
        supervisor = SupervisorAgent()
        researcher = ResearcherAgent()
        analyst = AnalystAgent()
        writer = WriterAgent()
        
        # Create StateGraph. Since LangGraph 0.2, it supports Pydantic models directly or dataclasses
        workflow = StateGraph(ResearchState)
        
        # Add nodes
        workflow.add_node("supervisor", supervisor.run)
        workflow.add_node("researcher", researcher.run)
        workflow.add_node("analyst", analyst.run)
        workflow.add_node("writer", writer.run)
        
        # Define edge routing based on state.route_history
        def route_next(state: ResearchState) -> str:
            if not state.route_history:
                return END
            next_node = state.route_history[-1]
            if next_node == "done":
                return END
            return next_node
            
        workflow.add_conditional_edges("supervisor", route_next)
        
        workflow.add_edge("researcher", "supervisor")
        workflow.add_edge("analyst", "supervisor")
        workflow.add_edge("writer", "supervisor")
        
        workflow.set_entry_point("supervisor")
        
        return workflow.compile()

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state."""
        app = self.build()
        final_state = app.invoke(state)
        # return the updated state object directly (langgraph with pydantic returns dict or pydantic, in v0.2 it might return dict, let's parse it)
        if isinstance(final_state, dict):
            return ResearchState(**final_state)
        return final_state  # type: ignore
