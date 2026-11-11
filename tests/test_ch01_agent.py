"""Chapter 1 — the TinyAgent skeleton."""

import pytest

from my_agent.agent import TinyAgent

# Chapter 2 gives __init__ an `llm` argument, so this whole file retires then.
pytestmark = [pytest.mark.chapter(1), pytest.mark.superseded(2)]


def test_component_slots_start_empty():
    agent = TinyAgent()
    assert agent.llm is None
    assert agent.memory is None
    assert agent.tools is None
    assert agent.planner is None


def test_run_echoes_the_task_without_a_brain():
    assert TinyAgent().run("What is 2 + 2?") == "Received: What is 2 + 2?"


def test_step_is_what_run_delegates_to():
    assert TinyAgent()._step("hi") == "Received: hi"


def test_execute_action_is_a_placeholder():
    assert TinyAgent()._execute_action("search") == "Executed action: search"
