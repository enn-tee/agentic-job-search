"""Base agent class with Claude integration."""

from abc import ABC, abstractmethod
from typing import Optional
import anthropic
import os


class BaseAgent(ABC):
    """Base class for all agents."""

    def __init__(
        self,
        name: str,
        model: str = "claude-sonnet-4-20250514",
        api_key: Optional[str] = None,
    ):
        """
        Initialize the base agent.

        Args:
            name: Agent name for logging
            model: Claude model to use
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.name = name
        self.model = model
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")

        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY must be set in environment or passed to agent"
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def _call_claude(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 4096,
        temperature: float = 1.0,
    ) -> str:
        """
        Call Claude API with given prompts.

        Args:
            system_prompt: System prompt defining agent behavior
            user_message: User message to process
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature

        Returns:
            Claude's response text
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )
            return message.content[0].text

        except Exception as e:
            raise RuntimeError(f"{self.name} failed to call Claude API: {e}")

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Execute the agent's main task.

        Must be implemented by subclasses.
        """
        pass

    def log(self, message: str):
        """Log a message with agent name prefix."""
        print(f"[{self.name}] {message}")
