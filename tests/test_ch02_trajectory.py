"""Chapter 2 — Step and Trajectory."""

import pytest

from conftest import fake_response
from my_agent.trajectory import Step, Trajectory

pytestmark = pytest.mark.chapter(2)


def test_step_defaults():
    s = Step()
    assert s.thought == ""
    assert s.action is None
    assert s.observation is None
    assert s.answer is None
    assert s.metadata is None


def test_trajectory_starts_empty():
    assert Trajectory().runs == []


def test_initialize_opens_a_run():
    t = Trajectory()
    t.initialize("What is 2 + 2?")
    assert t.runs == [{"query": "What is 2 + 2?", "steps": []}]


def test_add_without_observation_records_an_answer():
    t = Trajectory()
    t.initialize("q")
    t.add(fake_response(content="4", reasoning="2 + 2", metadata={"model": "m"}))
    (step,) = t.runs[0]["steps"]
    assert isinstance(step, Step)
    assert step.answer == "4"
    assert step.thought == "2 + 2"
    assert step.metadata == {"model": "m"}
    assert step.action is None and step.observation is None


def test_missing_reasoning_becomes_empty_thought():
    t = Trajectory()
    t.initialize("q")
    t.add(fake_response(content="4"))
    assert t.runs[0]["steps"][0].thought == ""


def test_add_with_observation_records_an_action():
    call = {"function": {"name": "get_weather", "arguments": "{}"}}
    t = Trajectory()
    t.initialize("q")
    t.add(fake_response(content="", tool_call=call), observation="Sunny, 21°C")
    (step,) = t.runs[0]["steps"]
    assert step.action == call
    assert step.observation == "Sunny, 21°C"
    assert step.answer is None


def test_steps_go_to_the_latest_run():
    t = Trajectory()
    t.initialize("first")
    t.add(fake_response(content="a"))
    t.initialize("second")
    t.add(fake_response(content="b"))
    t.add(fake_response(content="c"))
    assert [len(run["steps"]) for run in t.runs] == [1, 2]
