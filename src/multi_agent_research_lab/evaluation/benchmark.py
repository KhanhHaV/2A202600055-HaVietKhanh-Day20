"""Benchmark skeleton for single-agent vs multi-agent."""

from collections.abc import Callable
from time import perf_counter

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState

Runner = Callable[[str], ResearchState]


def run_benchmark(run_name: str, query: str, runner: Runner) -> tuple[ResearchState, BenchmarkMetrics]:
    started = perf_counter()
    state = runner(query)
    latency = perf_counter() - started
    
    total_cost = 0.0
    for res in state.agent_results:
        total_cost += res.metadata.get("cost_usd", 0.0)
        
    metrics = BenchmarkMetrics(
        run_name=run_name, 
        latency_seconds=latency,
        estimated_cost_usd=total_cost,
        quality_score=None # Optional LLM-as-a-judge could go here
    )
    return state, metrics
