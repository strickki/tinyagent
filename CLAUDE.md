# TinyAgent sandbox for *An Illustrated Guide to AI Agents*

The learner builds TinyAgent **by hand** here while reading the book. The authors' repo is a separate, untouched clone at `../An-Illustrated-Guide-To-AI-Agents` (the **reference**). `uv sync` installs it into this repo's environment as an editable `illustrated-agents` package.

- `src/my_agent/` is **the learner's code.** You write the scaffolding (stubs, hints, `TODO(chN)` markers); the learner writes the implementations. When they ask for help, coach first: point at the failing test, explain the concept, give a hint. Write a solution only when they explicitly ask for the answer.
- The **reference** is used for reading and validation, and stays exactly as cloned: no edits, no branches, no files added. `git pull` there is the only change it ever sees.
- `workbook/chapterNN/` holds notebook copies built from the reference's `chapterNN/`; they run the learner's code. `workbook/images/` is a copy of the reference's `images/`, so the notebooks' `../images/...` links resolve.
- `tests/` is gated by chapter: `uv run pytest --chapter N` runs chapters ≤ N and skips tests marked `superseded(M)` for M ≤ N.

To scaffold a new chapter, use the `scaffold-chapter` skill.
