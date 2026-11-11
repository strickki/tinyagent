"""Inspect and rewrite the book's notebooks into workbook copies. Stdlib only.

    python nbtool.py list  <notebook.ipynb>
    python nbtool.py build <source.ipynb> <spec.json> <out.ipynb>

`list` prints every cell's index, type, and opening lines (images elided).

`build` copies the source notebook, clears every output, and applies a spec:

    {
      "drop":    [3, 4],                                  # cell indices to remove
      "replace": {"16": [{"type": "markdown", "source": "..."},
                         {"type": "code",     "source": "..."}]},
      "insert_after": {"0": [{"type": "markdown", "source": "..."}]},
      "rewrite": [["from illustrated_agents.chapters.ch2 import LLM",
                   "from my_agent.llm import LLM"]]       # literal find/replace, code cells
    }

Indices always refer to the *source* notebook, so `list` output stays valid
while you write the spec. A `replace` value is a list of cells (one or many).
`rewrite` runs on every surviving source code cell, never on cells the spec inserts.
"""

import json
import re
import sys


def _cell(kind, source):
    cell = {"cell_type": kind, "metadata": {}, "source": source.splitlines(keepends=True)}
    if kind == "code":
        cell.update(execution_count=None, outputs=[])
    return cell


def list_cells(path):
    nb = json.load(open(path))
    for i, c in enumerate(nb["cells"]):
        src = re.sub(r"<img[^>]*>", "<img>", "".join(c["source"])).strip()
        head = "\n      ".join(src.splitlines()[:4])
        print(f"[{i}] {c['cell_type']}: {head}\n")


def build(src_path, spec_path, out_path):
    nb = json.load(open(src_path))
    spec = json.load(open(spec_path))
    drop = set(spec.get("drop", []))
    replace = {int(k): v for k, v in spec.get("replace", {}).items()}
    after = {int(k): v for k, v in spec.get("insert_after", {}).items()}
    rewrites = spec.get("rewrite", [])

    for i in list(drop) + list(replace) + list(after):
        if not 0 <= i < len(nb["cells"]):
            sys.exit(f"spec names cell {i}, but the notebook has {len(nb['cells'])} cells")

    cells = []
    for i, c in enumerate(nb["cells"]):
        if i in replace:
            cells += [_cell(n["type"], n["source"]) for n in replace[i]]
        elif i not in drop:
            if c["cell_type"] == "code":
                src = "".join(c["source"])
                for old, new in rewrites:
                    src = src.replace(old, new)
                c = {**c, "source": src.splitlines(keepends=True),
                     "outputs": [], "execution_count": None}
            cells.append(c)
        cells += [_cell(n["type"], n["source"]) for n in after.get(i, [])]

    nb["cells"] = cells
    nb["metadata"].pop("widgets", None)  # stale widget state from the authors' run
    with open(out_path, "w") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {out_path}: {len(cells)} cells")


if __name__ == "__main__":
    cmd, *args = sys.argv[1:] or ["help"]
    if cmd == "list" and len(args) == 1:
        list_cells(*args)
    elif cmd == "build" and len(args) == 3:
        build(*args)
    else:
        sys.exit(__doc__)
