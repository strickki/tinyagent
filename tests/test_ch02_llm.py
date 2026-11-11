"""Chapter 2 — Response and the LLM wrapper (no real server needed)."""

import pytest

from conftest import completion_payload
from my_agent.llm import LLM, Response

pytestmark = pytest.mark.chapter(2)


# ── Response ─────────────────────────────────────────────────────────────────


def test_response_defaults():
    r = Response()
    assert r.content == ""
    assert r.reasoning is None
    assert r.tool_call is None
    assert r.metadata is None


def test_response_holds_fields():
    r = Response(content="hi", reasoning="hmm", tool_call={"name": "x"}, metadata={})
    assert (r.content, r.reasoning, r.tool_call, r.metadata) == (
        "hi",
        "hmm",
        {"name": "x"},
        {},
    )


# ── LLM.__init__ ─────────────────────────────────────────────────────────────


def test_llm_defaults_target_local_ollama():
    llm = LLM(model="gemma3:12b")
    assert llm.model == "gemma3:12b"
    assert llm.base_url == "http://localhost:11434/v1"
    assert llm.api_key == "no_key"
    assert llm.think is False
    assert llm.temperature is None


# ── LLM.generate: the request ────────────────────────────────────────────────

MESSAGES = [{"role": "user", "content": "Hi! How's life?"}]


def test_posts_to_chat_completions(fake_server):
    LLM(model="m", base_url="http://example.test/v1").generate(MESSAGES)
    request = fake_server.requests[-1]
    assert request.full_url == "http://example.test/v1/chat/completions"
    assert request.get_method() == "POST"


def test_sends_json_with_bearer_auth(fake_server):
    LLM(model="m", api_key="sk-123").generate(MESSAGES)
    request = fake_server.requests[-1]
    assert request.get_header("Content-type") == "application/json"
    assert request.get_header("Authorization") == "Bearer sk-123"


def test_body_carries_model_and_messages(fake_server):
    LLM(model="gemma3:12b").generate(MESSAGES)
    body = fake_server.body()
    assert body["model"] == "gemma3:12b"
    assert body["messages"] == MESSAGES


@pytest.mark.parametrize("think, effort", [(False, "none"), (True, "medium")])
def test_think_maps_to_reasoning_effort(fake_server, think, effort):
    LLM(model="m", think=think).generate(MESSAGES)
    assert fake_server.body()["reasoning_effort"] == effort


def test_temperature_only_sent_when_set(fake_server):
    LLM(model="m").generate(MESSAGES)
    assert "temperature" not in fake_server.body()
    LLM(model="m", temperature=0).generate(MESSAGES)
    assert fake_server.body()["temperature"] == 0


def test_tools_only_sent_when_given(fake_server):
    LLM(model="m").generate(MESSAGES)
    assert "tools" not in fake_server.body()
    tools = [{"type": "function", "function": {"name": "get_weather"}}]
    LLM(model="m").generate(MESSAGES, tools=tools)
    assert fake_server.body()["tools"] == tools


# ── LLM.generate: parsing the reply ──────────────────────────────────────────


def test_returns_a_response_with_content(fake_server):
    fake_server.payload = completion_payload(content="Life is good.")
    response = LLM(model="m").generate(MESSAGES)
    assert isinstance(response, Response)
    assert response.content == "Life is good."


def test_no_reasoning_or_tool_call_when_absent(fake_server):
    response = LLM(model="m").generate(MESSAGES)
    assert response.reasoning is None
    assert response.tool_call is None


@pytest.mark.parametrize("key", ["reasoning", "reasoning_content"])
def test_reads_reasoning_under_either_key(fake_server, key):
    fake_server.payload = completion_payload(reasoning="9 - 2 + 4 = 11", reasoning_key=key)
    assert LLM(model="m").generate(MESSAGES).reasoning == "9 - 2 + 4 = 11"


def test_keeps_only_the_first_tool_call(fake_server):
    calls = [{"id": "a", "function": {"name": "one"}}, {"id": "b", "function": {"name": "two"}}]
    fake_server.payload = completion_payload(content=None, tool_calls=calls)
    assert LLM(model="m").generate(MESSAGES).tool_call == calls[0]


def test_metadata_has_model_and_token_counts(fake_server):
    fake_server.payload = completion_payload(model="gemma3:12b", prompt_tokens=5, completion_tokens=3)
    assert LLM(model="m").generate(MESSAGES).metadata == {
        "model": "gemma3:12b",
        "prompt_tokens": 5,
        "completion_tokens": 3,
    }
