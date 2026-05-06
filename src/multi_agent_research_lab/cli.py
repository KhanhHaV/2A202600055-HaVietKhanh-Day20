"""Command-line entrypoint for the lab starter."""

from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel

from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow
from multi_agent_research_lab.observability.logging import configure_logging

app = typer.Typer(help="Multi-Agent Research Lab starter CLI")
console = Console()


def _init() -> None:
    from dotenv import load_dotenv
    load_dotenv()
    settings = get_settings()
    configure_logging(settings.log_level)


@app.command()
def baseline(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run a minimal single-agent baseline placeholder."""

    _init()
    request = ResearchQuery(query=query)
    state = ResearchState(request=request)
    from multi_agent_research_lab.evaluation.benchmark import run_benchmark
    from multi_agent_research_lab.services.llm_client import LLMClient
    
    def runner(q: str) -> ResearchState:
        s = ResearchState(request=ResearchQuery(query=q))
        llm = LLMClient()
        response = llm.complete("You are a helpful assistant.", f"Answer the query: {q}")
        s.final_answer = response.content
        return s

    state, metrics = run_benchmark("baseline", query, runner)
    
    console.print(Panel.fit(state.final_answer or "", title=f"Single-Agent Baseline (Latency: {metrics.latency_seconds:.2f}s)"))


@app.command("multi-agent")
def multi_agent(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run the multi-agent workflow skeleton."""

    _init()
    from multi_agent_research_lab.evaluation.benchmark import run_benchmark
    
    def runner(q: str) -> ResearchState:
        s = ResearchState(request=ResearchQuery(query=q))
        w = MultiAgentWorkflow()
        return w.run(s)

    try:
        result, metrics = run_benchmark("multi_agent", query, runner)
        console.print(f"Latency: {metrics.latency_seconds:.2f}s, Estimated Cost: ${metrics.estimated_cost_usd:.4f}")
    except StudentTodoError as exc:
        console.print(Panel.fit(str(exc), title="Expected TODO", style="yellow"))
        raise typer.Exit(code=2) from exc
    console.print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    app()
