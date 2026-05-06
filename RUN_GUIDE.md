# Run Guide: Lab 20 - Multi-Agent Research System

This guide provide detailed steps to configure and run the multi-agent research system lab.

## 1. System Requirements

- Python 3.11+
- Virtual environment (venv)

## 2. Installation

Activate your virtual environment and install the necessary dependencies. The `pyproject.toml` file has been updated to support **Google GenAI** (`langchain-google-genai`).

Open your terminal in the project root directory (`e:\vinai\2A202600055-HaVietKhanh-Day20`) and run:

```bash
python -m venv .venv
# Activate venv (on Windows)
.venv\Scripts\activate
# Install dependencies
pip install -e ".[dev,llm]"
```

## 3. Environment Configuration

The `.env` file has been created from `.env.example`. Your API Key (Google/Vertex API key) has been automatically added as `GOOGLE_API_KEY`.

If you want to change the model (default is `gemini-2.5-flash`), add the following line to your `.env` file:

```env
GOOGLE_MODEL=gemini-2.5-pro
```

## 4. Run Single-Agent Baseline

Use the following command to run the system in **Single-Agent Baseline** mode (direct LLM call, no LangGraph):

```bash
python -m multi_agent_research_lab.cli baseline --query "Research GraphRAG state-of-the-art"
```

## 5. Run Multi-Agent System

This command starts the full LangGraph workflow through the agents:
**Supervisor -> Researcher -> Analyst -> Writer -> Supervisor -> End**.

```bash
python -m multi_agent_research_lab.cli multi-agent --query "Research GraphRAG state-of-the-art"
```

The system will output the Latency, Estimated Cost (based on tokens), and a JSON string containing the routing history and the final answer.

## 6. Run Unit Tests and Linting

To verify that your changes satisfy the basic requirements and standards:

```bash
# Run unit tests
pytest

# Run linting (Ruff)
ruff check src tests

# Run type checking (Mypy)
mypy src
```

## Tracing Notes

If you have a LangSmith account, add `LANGSMITH_API_KEY` to your `.env` file. The system has built-in observability hooks; all queries and graph executions will be recorded in your LangSmith dashboard.
