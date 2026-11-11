"""trajectory.py — a record of everything the agent did (Chapter 2).

Agents can run for many steps; the trajectory is how you debug them.
`illustrated_agents.utils.TrajectoryViewer(agent.trajectory)` renders yours
in a notebook, as long as you keep the shapes described below.

Check yourself:  uv run pytest --chapter 2 -k trajectory
"""

from dataclasses import dataclass


@dataclass
class Step:
    """A single step in an agent's trajectory.

    Mirrors `Response`, but in THOUGHT / ACTION / OBSERVATION / ANSWER terms
    (the loop you'll build in Chapter 6).

    TODO(ch2): add five fields:
      thought      reasoning text (defaults to an empty string)
      action       the tool call the agent made (dict), if any
      observation  what the tool returned (str), if any
      answer       the final answer (str), if this step ended the turn
      metadata     dict of extra info, if any
    Everything except `thought` defaults to None.
    """


class Trajectory:
    """Records agent execution as a sequence of runs.

    Shape (the viewer relies on it):
        self.runs == [{"query": <str>, "steps": [Step, Step, ...]}, ...]
    """

    def __init__(self) -> None:
        # TODO(ch2): start with no runs.
        raise NotImplementedError

    def initialize(self, query: str) -> None:
        """Register a new run with the given query."""
        # TODO(ch2)
        raise NotImplementedError

    def add(self, response, observation: str | None = None) -> None:
        """Record a step from a Response, optionally with an observation.

        TODO(ch2):
          * The step's thought comes from the response's reasoning (or "" if
            there was none); its metadata from the response's metadata.
          * With an observation, the step is an ACTION/OBSERVATION pair: the
            action is the response's tool call.
          * Without one, it is a final ANSWER: the response's content.
          * Append the step to the most recent run.
        """
        raise NotImplementedError
