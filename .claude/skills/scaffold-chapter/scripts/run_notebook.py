"""Execute a notebook in memory (the file on disk is left untouched).

    uv run python run_notebook.py <notebook.ipynb>

Runs with the notebook's own folder as the working directory and prints the
output of any cell that runs pytest. Raises on the first failing cell.
"""

import os
import sys

import nbformat
from nbclient import NotebookClient

path = sys.argv[1]
nb = nbformat.read(path, as_version=4)
NotebookClient(
    nb, timeout=180, kernel_name="python3",
    resources={"metadata": {"path": os.path.dirname(os.path.abspath(path))}},
).execute()
for cell in nb.cells:
    if cell.cell_type == "code" and "pytest" in cell.source:
        print("".join(o.get("text", "") for o in cell.outputs)[-300:])
print("executed OK:", path)
