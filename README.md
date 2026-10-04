# ID2221 reading assignment

Essay and video materials for the ID2221 (KTH, HT26) reading assignment on:

> A. Radovanović et al., "Carbon-Aware Computing for Datacenters," *IEEE Transactions on Power Systems*, vol. 38, no. 2, pp. 1270-1280, 2023. Preprint: [arXiv:2106.11750](https://arxiv.org/abs/2106.11750).

| Path | What it is |
|---|---|
| `essay/essay.md`, `essay/essay.pdf` | The two-page essay (summary, approach, critical reflection) |
| `presentation/slides-and-script.md`, `.pdf` | Slide-by-slide content and speaker notes for the 10-15 minute video |
| `presentation/figures/` | Figures cropped from the paper, for use on slides |
| `notes/research-notes.md` | Facts with page references, the counter-paper, and a pre-submission checklist |
| `build/` | Markdown to PDF script and stylesheets |

## Rebuilding the PDFs

```
pip install markdown
python3 build/build_pdf.py essay/essay.md presentation/slides-and-script.md notes/research-notes.md
```

The script uses headless Chromium. Set `CHROME=/path/to/chrome` if it is not at the default Playwright location.
