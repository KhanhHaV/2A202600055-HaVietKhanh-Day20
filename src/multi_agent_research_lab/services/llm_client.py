"""LLM client abstraction.

Production note: agents should depend on this interface instead of importing an SDK directly.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LLMResponse:
    content: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None


class LLMClient:
    """Provider-agnostic LLM client skeleton."""

    def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Return a model completion."""
        import logging
        import os

        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Default model is gemini-1.5-flash
        model_name = os.getenv("GOOGLE_MODEL", "gemini-1.5-flash")
        
        try:
            llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
            messages = [
                ("system", system_prompt),
                ("human", user_prompt)
            ]
            
            response = llm.invoke(messages)
            
            input_tokens = 0
            output_tokens = 0
            
            if hasattr(response, "usage_metadata") and response.usage_metadata:
                input_tokens = response.usage_metadata.get("input_tokens", 0)
                output_tokens = response.usage_metadata.get("output_tokens", 0)
                
            # Estimated cost for gemini-1.5-flash
            cost = (input_tokens * 0.075 / 1_000_000) + (output_tokens * 0.3 / 1_000_000)
            
            return LLMResponse(
                content=str(response.content),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=cost
            )
        except Exception as e:
            logging.error(f"LLM call failed: {e}")
            raise
