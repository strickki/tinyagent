"""agent.py — your TinyAgent. This file grows a little every chapter.

Check yourself:  uv run pytest --chapter 1
"""


class TinyAgent:
    """A minimal, modular, and educational agent framework.

    ── Chapter 1 ────────────────────────────────────────────────────────────
    Build the skeleton. There is no LLM yet, so the agent can only echo.

    ── Chapter 2 (do this after the Chapter 1 tests pass) ───────────────────
    Give the agent its "brain" (see the diff in the book / workbook):
      * `__init__` takes an `llm` (your `my_agent.llm.LLM`) and stores it.
      * It also creates a `Trajectory` (from `my_agent.trajectory`) as
        `self.trajectory`.
      * `run` registers the task in the trajectory before stepping.
      * `_step` sends the task to the LLM as a single user message, records
        the response in the trajectory, and returns the response's content.
    Then `uv run pytest --chapter 2` — the Chapter 1 agent tests are
    marked as superseded and stop running at that point.
    """

    def __init__(self):
        # TODO(ch1): create the four component slots the book introduces —
        #   llm, memory, tools, planner — all empty (None) for now.
        #   A comment on each saying which chapter fills it in is a nice touch.
        raise NotImplementedError

    def run(self, task: str) -> str:
        """Run the agent on a task."""
        # TODO(ch1): an agent run is one or more steps. For now: one step.
        raise NotImplementedError

    def _step(self, task: str) -> str:
        """Perform a single step."""
        # TODO(ch1): no brain yet — return "Received: <task>".
        raise NotImplementedError

    def _execute_action(self, action: str) -> str:
        """Execute a tool action."""
        # TODO(ch1): placeholder until Chapter 5 — return "Executed action: <action>".
        raise NotImplementedError
