"""Render Markdown files to PDF with headless Chromium.

Usage: python3 build/build_pdf.py essay/essay.md [more.md ...]
Each input X.md produces X.pdf next to it. Needs `pip install markdown`
and a Chromium binary (set CHROME to override the path).
"""
import os
import pathlib
import subprocess
import sys
import tempfile

import markdown

ROOT = pathlib.Path(__file__).resolve().parent
CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")


def render(md_path: pathlib.Path) -> pathlib.Path:
    style = "essay.css" if md_path.parent.name == "essay" else "notes.css"
    css = (ROOT / style).read_text()
    body = markdown.markdown(md_path.read_text(), extensions=["tables", "sane_lists"])
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>"
    pdf_path = md_path.with_suffix(".pdf")
    # Write the HTML next to the source so relative image paths resolve.
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=md_path.parent, delete=False) as f:
        f.write(html)
        tmp = f.name
    try:
        subprocess.run(
            [CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
             f"--print-to-pdf={pdf_path}", f"file://{tmp}"],
            check=True, capture_output=True,
        )
    finally:
        os.unlink(tmp)
    return pdf_path


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print(render(pathlib.Path(arg).resolve()))
