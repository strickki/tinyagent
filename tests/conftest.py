"""Shared test plumbing.

Chapter gating
--------------
Every test file sets `pytestmark = pytest.mark.chapter(N)`. Tests describing
behaviour a later chapter replaces also carry `@pytest.mark.superseded(M)`.

    uv run pytest --chapter 2   # chapters <= 2, minus anything superseded by <= 2
    uv run pytest               # every chapter, minus anything superseded at all

Fakes
-----
Nothing here imports `my_agent`, so a half-written module never breaks
collection of the other chapters' tests.
"""

import io
import json
from types import SimpleNamespace

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--chapter",
        type=int,
        default=None,
        help="Run tests for chapters up to and including N (the chapter you're on).",
    )


def pytest_collection_modifyitems(config, items):
    upto = config.getoption("--chapter")
    deselected, kept = [], []
    for item in items:
        ch = item.get_closest_marker("chapter")
        sup = item.get_closest_marker("superseded")
        chapter = ch.args[0] if ch else 0
        superseded = sup.args[0] if sup else None
        if upto is None:
            drop = superseded is not None
        else:
            drop = chapter > upto or (superseded is not None and superseded <= upto)
        (deselected if drop else kept).append(item)
    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = kept


# ── Fake LLM ─────────────────────────────────────────────────────────────────


def fake_response(content="", reasoning=None, tool_call=None, metadata=None):
    """Duck-typed stand-in for `my_agent.llm.Response`."""
    return SimpleNamespace(
        content=content, reasoning=reasoning, tool_call=tool_call, metadata=metadata
    )


class FakeLLM:
    """Scripted LLM: returns the given replies in order and records every call.

    Replies may be strings (become `content`) or `fake_response(...)` objects.
    """

    def __init__(self, *replies):
        self._replies = list(replies)
        self.calls: list[dict] = []

    def generate(self, messages, tools=None):
        self.calls.append({"messages": messages, "tools": tools})
        if not self._replies:
            raise AssertionError("FakeLLM ran out of scripted replies")
        reply = self._replies.pop(0)
        return fake_response(content=reply) if isinstance(reply, str) else reply


@pytest.fixture
def make_llm():
    return FakeLLM


# ── Fake HTTP for the LLM wrapper ────────────────────────────────────────────


def completion_payload(
    content="Hello!",
    reasoning=None,
    reasoning_key="reasoning",
    tool_calls=None,
    model="test-model",
    prompt_tokens=11,
    completion_tokens=7,
):
    """An OpenAI-style /chat/completions response body."""
    message = {"role": "assistant", "content": content}
    if reasoning is not None:
        message[reasoning_key] = reasoning
    if tool_calls is not None:
        message["tool_calls"] = tool_calls
    return {
        "model": model,
        "choices": [{"index": 0, "message": message}],
        "usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens},
    }


@pytest.fixture
def fake_server(monkeypatch):
    """Patch `urllib.request.urlopen`; capture requests, serve a canned reply.

    Set `fake_server.payload` before calling the code under test, then inspect
    `fake_server.requests` (urllib `Request` objects) and `fake_server.body()`.
    """

    class Server:
        payload = completion_payload()
        requests: list = []

        def body(self, i=-1):
            return json.loads(self.requests[i].data)

    server = Server()
    server.requests = []

    def urlopen(request, *args, **kwargs):
        server.requests.append(request)
        return io.BytesIO(json.dumps(server.payload).encode())

    monkeypatch.setattr("urllib.request.urlopen", urlopen)
    return server
