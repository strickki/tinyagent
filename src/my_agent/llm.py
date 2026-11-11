"""llm.py — the agent's "brain" (Chapter 2).

Pure Python: talk to any OpenAI-compatible server (Ollama, LM Studio,
llama.cpp, OpenRouter, ...) with nothing but `json` and `urllib.request`.

Check yourself:  uv run pytest --chapter 2 -k llm
"""

import json  # noqa: F401  (you'll need these)
import urllib.request  # noqa: F401
from dataclasses import dataclass


@dataclass
class Response:
    """Structured response from LLM calls.

    Different servers return slightly different shapes; this dataclass is the
    one shape the rest of your agent sees.

    TODO(ch2): add four fields, all optional:
      content    the model's answer text (defaults to an empty string)
      reasoning  native "thinking" text, if the model produced any
      tool_call  the first tool call the model asked for (a dict), if any
      metadata   a dict of extra info (model name, token counts)
    """


class LLM:
    """Thin wrapper around an OpenAI-compatible `/chat/completions` endpoint."""

    def __init__(
        self,
        model: str,
        base_url: str = "http://localhost:11434/v1",
        api_key: str = "no_key",
        think: bool = False,
        temperature: float | None = None,
    ):
        """Initialize the LLM with the given model."""
        # TODO(ch2): store every argument as an attribute of the same name.
        raise NotImplementedError

    def generate(self, messages: list[dict], tools: list | None = None) -> Response:
        """Generate a response from the LLM given a list of messages.

        TODO(ch2), in four parts:

        1. Build the request body: `model` and `messages`, plus
           - `tools`, only when tools were given (used from Chapter 5),
           - `reasoning_effort`: "none" when thinking is off, "medium" when on,
           - `temperature`, only when one was set.

        2. POST the body as JSON to `<base_url>/chat/completions` with
           `Content-Type: application/json` and `Authorization: Bearer <api_key>`.
           Use `urllib.request.Request` + `urllib.request.urlopen(...)`
           (call it through the module like that — the tests patch it).

        3. Pull out of the first choice's `message`:
           - content
           - reasoning: servers disagree on the key — try `reasoning`, then
             `reasoning_content`
           - tool_call: the first entry of `tool_calls`, or None
           and build metadata from the top-level `model` and `usage`
           (`model`, `prompt_tokens`, `completion_tokens`).

        4. Return it all as a `Response`.
        """
        raise NotImplementedError
