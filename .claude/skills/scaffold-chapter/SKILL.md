---
name: scaffold-chapter
description: Scaffold a book chapter for the learner — stubs in src/my_agent, chapter-gated tests, a workbook notebook. Use when asked to scaffold, set up, or prepare chapter N.
---

# Scaffold a chapter

The learner reads *An Illustrated Guide to AI Agents* and types the code themselves. Scaffolding a chapter gives them three things: **stubs** to fill in, **tests** that state the contract, and a **workbook** notebook that runs *their* code. The authors' repo, cloned at `../An-Illustrated-Guide-To-AI-Agents` (`$REF` below), is the **reference** you read from and validate against. It stays exactly as cloned: every file you write goes in this sandbox. `uv sync` installs it here as the `illustrated_agents` package.

Chapters 1–3 are already scaffolded. They are the worked example for every convention below, so open them alongside this file: `src/my_agent/`, `tests/`, `workbook/`, and `specs/` in this skill folder.

Scripts live in `.claude/skills/scaffold-chapter/scripts/` (called `$S` below). Use the session scratchpad for throwaway files.

## 1. Inventory the chapter

Read every notebook in `$REF/chapterNN/` (some chapters have side notebooks, e.g. `chapter04_short_term_memory.ipynb`; `uv run python $S/nbtool.py list <nb>` gives a quick map), plus the reference `$REF/src/illustrated_agents/chapters/chN*.py`.

List every `class` and `def` the notebooks define, and give each a home:

- **Agent code.** It survives into the authors' final package (`$REF/src/illustrated_agents/<module>.py`, maybe renamed). It goes in `src/my_agent/<same module>.py`.
- **Exercise.** It is a chapter-only experiment (e.g. Ch 3's self-consistency, Ch 7's `Evaluator`). It goes in `src/my_agent/exercises/chNN.py`. Loose notebook loops that teach a technique become small testable functions here (see `exercises/ch03.py`).
- **Demo.** It is throwaway notebook glue. It stays in the notebook as is.

Done when every definition in every notebook of the chapter has a home.

## 2. Read the learner's current code

Open each `src/my_agent` file this chapter touches. Their implementations are theirs: extend the file and leave their method bodies as they wrote them. When a chapter changes an existing class (`TinyAgent` changes nearly every chapter), add a `── Chapter N ──` section to the class docstring that describes the change, plus `TODO(chN)` markers where new parameters or methods appear. `agent.py` shows this for Chapter 2. If their code has drifted from the book's interface in a way the new chapter depends on, tell the learner rather than adapting the tests silently.

## 3. Write the stubs

- **Signatures from the reference.** Copy the exact names, parameters, defaults, and type hints, so later chapters and the authors' viewers (`TrajectoryViewer`, `DiffViewer`) keep working with the learner's objects.
- **Body: `raise NotImplementedError`** under a `# TODO(chN): <hint>` comment.
- **Hints describe behaviour, never code.** Give the inputs, outputs, edge cases, and the contract the tests check, numbered in parts for longer methods (see `LLM.generate`). For dataclasses, list the fields and their meaning in the docstring and let the learner write them.
- **Module docstring** ends with `Check yourself:  uv run pytest --chapter N [-k ...]`.
- **Every stub imports cleanly**, so a half-written module never breaks collection of other chapters' tests.
- When a test must patch something (HTTP via `urllib.request.urlopen`), the hint tells the learner to call it through the module so the patch takes.
- Add the new module to the list in `src/my_agent/__init__.py`.

## 4. Write the tests

One file per module: `tests/test_chNN_<module>.py` with `pytestmark = pytest.mark.chapter(N)`.

- **Test the contract**: return values, recorded state, the messages sent to the LLM, the request body. Leave room for any reasonable implementation the hints allow.
- **Use the shared fakes in `tests/conftest.py`**: `make_llm` (a scripted `FakeLLM` that records `calls`), `fake_response`, and `fake_server` / `completion_payload` for HTTP. Extend conftest with new fakes (tool calls, embeddings) and keep it free of `my_agent` imports.
- **Supersede.** When this chapter changes behaviour an earlier test pins down, mark that test (or file) `@pytest.mark.superseded(N)`, so `--chapter N` drops it. Earlier tests carry guesses like `superseded(4)` in `test_ch02_agent.py`; confirm or correct each one against the actual chapter.

## 5. Validate: green on the reference, red on the stubs

Build a throwaway package in the scratchpad named `my_agent`, whose modules re-export the reference (`from illustrated_agents.chapters.chN import X`). For exercises, transcribe the notebook's own code. Run it with bytecode caching off, because rewriting a same-size file within a second serves stale `.pyc`:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<scratch>/refpkg uv run pytest -q -p no:cacheprovider --chapter N
```

Done when:
- every chapter-N test is green against the reference,
- earlier chapters' surviving tests are still green against the reference,
- every chapter-N test is red against the stubs with `NotImplementedError` and no import or collection errors (`uv run pytest --chapter N`), and
- for any earlier chapter, swapping in that chapter's reference agent turns its `--chapter` run green again.

When a test fails on the reference, the test is wrong. Fix the test.

## 6. Build the workbook

Write a spec (format: `nbtool.py` docstring; examples: `specs/ch0*.json`). Save it as `specs/chNN.json`, then build each chapter notebook into `workbook/chapterNN/`:

```bash
uv run python $S/nbtool.py build $REF/chapterNN/<nb>.ipynb .claude/skills/scaffold-chapter/specs/chNN.json workbook/chapterNN/<nb>.ipynb
```

`workbook/images/` mirrors `$REF/images/`, so the notebooks' `../images/...` links resolve. Copy over any image the new chapter links that is missing.

Spec conventions:
- **Drop** the Colab install / GPU cells.
- **Insert after cell 0** the header markdown and the `%autoreload` cell (copy them from `specs/ch02.json`, changing the chapter number).
- **Replace each agent-code or exercise definition cell** with a `**✏️ YOUR TURN** — implement X in **`src/my_agent/...`**.` markdown cell plus a code cell that imports the learner's version.
- **Rewrite imports** of earlier chapters' learner-built objects (`from illustrated_agents.chapters.chM import LLM`) to `my_agent`, keeping the authors' display helpers (`illustrated_agents.utils`).
- **Annotated / diff / overview cells stay** as the authors' reference, prefixed with a `# 📖 authors' solution` comment line via `rewrite`.
- **End with the ✅ Check & compare cells**: a `!cd ../.. && uv run pytest --chapter N -q` cell, and `DiffViewer(<authors' class>, <learner's class>)` for each agent-code class.

Execute every workbook against the reference package, with `$S/fake_server.py` standing in for Ollama when nothing is listening on `localhost:11434`. Extend the fake server's `reply()` when a chapter needs tool calls or embeddings.

```bash
uv run python $S/fake_server.py &   # note the PID; kill it afterwards
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<scratch>/refpkg uv run python $S/run_notebook.py workbook/chapterNN/<nb>.ipynb
```

Done when every workbook notebook of the chapter executes without error and its check cell is green.

## 7. Hand over

Add the chapter's row to the Status table in `README.md`. Leave the work uncommitted so the learner can review it, and tell them:
- the files to implement, in the order the chapter introduces them,
- the test command,
- the earlier tests that are now superseded, and
- any judgment call you made: where a definition went in step 1, and any interface drift found in step 2.
