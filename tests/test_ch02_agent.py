"""Chapter 2 — TinyAgent gets a brain."""

import pytest

from my_agent.agent import TinyAgent
from my_agent.trajectory import Trajectory

pytestmark = pytest.mark.chapter(2)


def test_agent_stores_its_llm(make_llm):
    llm = make_llm()
    agent = TinyAgent(llm=llm)
    assert agent.llm is llm


@pytest.mark.superseded(4)  # Chapter 4 fills the memory slot (adjust when scaffolding ch4)
def test_other_slots_still_empty(make_llm):
    agent = TinyAgent(llm=make_llm())
    assert agent.memory is None
    assert agent.tools is None
    assert agent.planner is None


def test_agent_owns_a_trajectory(make_llm):
    assert isinstance(TinyAgent(llm=make_llm()).trajectory, Trajectory)


def test_run_returns_the_llm_answer(make_llm):
    agent = TinyAgent(llm=make_llm("4"))
    assert agent.run("What is 2 + 2?") == "4"


def test_task_goes_to_the_llm_as_one_user_message(make_llm):
    llm = make_llm("4")
    TinyAgent(llm=llm).run("What is 2 + 2?")
    assert llm.calls[0]["messages"] == [{"role": "user", "content": "What is 2 + 2?"}]


def test_run_is_recorded_in_the_trajectory(make_llm):
    agent = TinyAgent(llm=make_llm("4"))
    agent.run("What is 2 + 2?")
    (run,) = agent.trajectory.runs
    assert run["query"] == "What is 2 + 2?"
    assert [step.answer for step in run["steps"]] == ["4"]


def test_each_run_gets_its_own_entry(make_llm):
    agent = TinyAgent(llm=make_llm("a", "b"))
    agent.run("one")
    agent.run("two")
    assert [run["query"] for run in agent.trajectory.runs] == ["one", "two"]
