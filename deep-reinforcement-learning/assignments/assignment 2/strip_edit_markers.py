"""Remove the [EDIT n] review markers from the solution notebook.

Run this from this folder once the changes have been reviewed, before the final
full-mode run:

    python strip_edit_markers.py

It deletes, in place:
  * the "Change log for this revision" cell at the top of the notebook;
  * every code comment line that starts with "# [EDIT " (each marker is exactly
    one line, so the ordinary comments below it are always kept);
  * the "<!-- [EDIT ... -->" note at the top of each rewritten markdown cell.

No code, output or ordinary comment is touched, so the notebook still runs
exactly as it does now.
"""
import json
import re
from pathlib import Path

NOTEBOOK = Path(__file__).with_name("Vivek_Group_95_Q_learning_DQN_DDQN_Solution.ipynb")
LEGEND_CELL_ID = "edit0legend"

# A code marker is a whole comment line, possibly indented, and never spans lines.
CODE_MARKER = re.compile(r"^\s*#\s*\[EDIT\b")
# A markdown marker is a single HTML comment, invisible when the cell is rendered.
MARKDOWN_MARKER = re.compile(r"<!--\s*\[EDIT\b.*?-->\s*\n?")


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    removed_cells = 0
    removed_markers = 0
    kept_cells = []

    for cell in notebook["cells"]:
        # Drop the change-log cell entirely.
        if cell.get("id") == LEGEND_CELL_ID:
            removed_cells += 1
            continue

        if cell["cell_type"] == "code":
            kept_lines = [ln for ln in cell["source"] if not CODE_MARKER.match(ln)]
            removed_markers += len(cell["source"]) - len(kept_lines)
            cell["source"] = kept_lines
        else:
            text = "".join(cell["source"])
            stripped = MARKDOWN_MARKER.sub("", text)
            if stripped != text:
                removed_markers += 1
                lines = stripped.split("\n")
                cell["source"] = [ln + "\n" for ln in lines[:-1]] + [lines[-1]]

        kept_cells.append(cell)

    notebook["cells"] = kept_cells
    NOTEBOOK.write_text(
        json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Removed {removed_cells} change-log cell and {removed_markers} markers.")
    print("Next: set RUN_MODE = 'full', restart the kernel, and run all cells.")


if __name__ == "__main__":
    main()
