# TinyAgent: built by hand

An AI agent built from scratch, one chapter at a time, while reading
[*An Illustrated Guide to AI Agents*](https://www.oreilly.com/library/view/an-illustrated-guide/9798341662681/)
by Maarten Grootendorst and Jay Alammar.

The book's [companion repo](https://github.com/HandsOnLLM/An-Illustrated-Guide-To-AI-Agents)
ships the finished `TinyAgent`. This repo turns it into a **skeleton**: every
module starts as a stub with hints, every chapter comes with tests that state
what the code must do, and the book's notebooks are rewired to run *my*
implementation instead of the authors'.

## How it works

| Piece | Where | What it gives you |
|---|---|---|
| **Stubs** | `src/my_agent/` | The book's exact signatures, docstrings that describe the behaviour (never the code), and `TODO(chN)` markers. Bodies raise `NotImplementedError` until you write them. |
| **Tests** | `tests/` | The contract for each chapter. The LLM and its HTTP server are faked, so the tests run in well under a second with no model. |
| **Workbooks** | `workbook/chapterNN/` | The book's notebooks: **✏️ YOUR TURN** cells point at the stub to write, 📖 cells show the authors' solution when you want to peek, and the last cells diff your code against theirs. |

The authors' repo is kept as an untouched **reference** clone next to this one.
`uv sync` installs it as the `illustrated_agents` package, which supplies the
notebook display helpers and the per-chapter reference code the tests are
checked against.

```
Projects/
├── An-Illustrated-Guide-To-AI-Agents/   reference clone (never edited)
└── tinyagent/                           this repo
    ├── src/my_agent/                    my implementation
    │   ├── agent.py                     TinyAgent (grows every chapter)
    │   ├── llm.py                       Ch 2: LLM wrapper + Response
    │   ├── trajectory.py                Ch 2: Step + Trajectory
    │   └── exercises/                   chapter-only experiments (Ch 3, ...)
    ├── tests/                           test_chNN_*.py + shared fakes in conftest.py
    ├── workbook/                        chapterNN/*.ipynb + the book's images
    └── .claude/skills/scaffold-chapter/ how new chapters get scaffolded
```

## Setup

Needs [uv](https://docs.astral.sh/uv/) and, for the notebooks, an OpenAI-compatible
model server (the defaults assume [Ollama](https://ollama.com) on `localhost:11434`).

```bash
git clone https://github.com/HandsOnLLM/An-Illustrated-Guide-To-AI-Agents.git
git clone https://github.com/strickki/tinyagent.git
cd tinyagent
uv sync                      # my package + the authors' (from the clone) + Jupyter + pytest

ollama pull gemma3:12b       # prompting-based examples
ollama pull gemma4:e4b       # native reasoning / tool calling
```

## The loop, per chapter

1. Read the chapter.
2. Fill in the `TODO(chN)` stubs in `src/my_agent/`.
3. `uv run pytest --chapter N` until it's green.
4. `uv run jupyter lab` and work through `workbook/chapterNN/` against a real model.
5. Commit and tag it: `git tag chN-done`.

### Chapter-gated tests

Every test file is marked with its chapter. `--chapter N` runs everything up to
chapter N, so later chapters stay quiet until you get there:

```bash
uv run pytest --chapter 2            # chapters 1–2
uv run pytest --chapter 2 -k llm     # just the LLM wrapper
```

When a later chapter changes an interface (Chapter 2 gives `TinyAgent` an
`llm` argument, for example), the older tests are marked `superseded(N)` and
drop out once you pass `--chapter N`.

## Progress

| Ch | Topic | Scaffolded | Implemented | Files |
|---|---|:---:|:---:|---|
| 1 | Introduction to AI agents | ✅ | ⬜ | `agent.py` |
| 2 | Large language models | ✅ | ⬜ | `llm.py`, `trajectory.py`, `agent.py` |
| 3 | Reasoning LLMs | ✅ | ⬜ | `exercises/ch03.py` |
| 4 | Memory | ⬜ | ⬜ | |
| 5 | Tools | ⬜ | ⬜ | |
| 6 | Planning | ⬜ | ⬜ | |
| 7 | Evaluation | ⬜ | ⬜ | |
| 8 | Multi-agent collaboration | ⬜ | ⬜ | |
| 9 | Multimodal understanding | ⬜ | ⬜ | |
| 10 | Coding agents | ⬜ | ⬜ | |

## Scaffolding the next chapter

Chapters are scaffolded as I reach them, so nothing gets spoiled ahead of time.
In [Claude Code](https://claude.com/claude-code), ask it to *"scaffold chapter N"*.
The project skill in [`.claude/skills/scaffold-chapter/`](.claude/skills/scaffold-chapter/SKILL.md)
holds the procedure:

1. Inventory every class and function the chapter defines.
2. Write stubs, extending my existing code without overwriting it.
3. Write tests, and check that they pass on the authors' code and fail on the stubs.
4. Build the workbook notebooks, and run them end to end on the authors' code against a fake LLM server.

[`CLAUDE.md`](CLAUDE.md) sets the ground rules: `src/my_agent` is mine to write,
and Claude coaches instead of handing over solutions.

## Credits

- **Book:** *An Illustrated Guide to AI Agents*, Maarten Grootendorst & Jay
  Alammar (O'Reilly, 2026).
- **Companion code:** [HandsOnLLM/An-Illustrated-Guide-To-AI-Agents](https://github.com/HandsOnLLM/An-Illustrated-Guide-To-AI-Agents),
  MIT-licensed (as declared in its `pyproject.toml`). The notebooks in `workbook/` are adapted from the
  authors' notebooks, the images in `workbook/images/` are theirs, and the
  interfaces the stubs follow come from their `TinyAgent`. All credit for that
  material goes to them.
- **Everything else** (stubs, tests, tooling) was written for this repo.
