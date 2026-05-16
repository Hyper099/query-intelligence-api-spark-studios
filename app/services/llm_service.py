import logging
from pathlib import Path

import anthropic
from jinja2 import Template

from app.config import Settings

logger = logging.getLogger(__name__)


class LLMServiceError(RuntimeError):
    """Raised when Claude cannot return a usable response."""


class LLMService:

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        self.client = anthropic.Anthropic(
            api_key=settings.anthropic_api_key,
            timeout=settings.anthropic_timeout_seconds,
            max_retries=settings.anthropic_max_retries,
        )

        prompt_path = Path(settings.prompt_template_path)
        self.prompt_template = Template(prompt_path.read_text(encoding="utf-8"))

    def extract_query(self, query: str) -> str:
        """Send a normalized query to Claude and return raw response text."""

        if not self.settings.anthropic_api_key:
            raise LLMServiceError("ANTHROPIC_API_KEY is not configured")

        prompt = self.prompt_template.render(
            query=query,
            prompt_version=self.settings.prompt_version,
        )

        try:
            response = self.client.messages.create(
                model=self.settings.anthropic_model,
                max_tokens=400,
                temperature=0,
                messages=[{"role": "user", "content": prompt}],
            )

            return response.content[0].text.strip()
        except Exception as exc:
            logger.warning("claude_extraction_failed", exc_info=exc)
            raise LLMServiceError("Failed to extract structured query") from exc
