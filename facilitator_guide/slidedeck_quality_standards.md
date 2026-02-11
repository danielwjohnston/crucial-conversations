# Slidedeck Quality Standards

This checklist defines a cohesive baseline for every chapter deck and uses **chapter 10 (Retake Your Pen)** as the benchmark for facilitation flow.

## 1) Learning design standards

Each chapter should include:
- **Context slide**: what chapter skill solves and when to use it.
- **Model slide(s)**: core framework language from the source text.
- **Demonstration/example slide(s)**: practical, realistic workplace scenarios.
- **Discussion prompt**: explicit group reflection/debrief question.
- **Action commitment**: clear behavior to practice before the next session.

## 2) Facilitation standards

- Keep a predictable cadence: concept → example → practice → debrief → commitment.
- Include at least one pair/small-group prompt every chapter.
- Include a clear “what to do next week” action statement.
- Preserve psychologically safe language and avoid shaming phrasing.

## 3) Technical and accessibility standards

- Keyboard navigable controls and visible focus states.
- Reduced-motion support for animated transitions.
- Skip link and semantic heading order.
- Legible contrast and readable text density (avoid walls of text).

## 4) Content integrity standards

- Validate chapter deck alignment to the corresponding source `.txt` file in `original_files/`.
- Keep terminology consistent across chapters (especially skill labels and framework names).
- Avoid introducing unsupported claims not present in source content.

## 5) Required QA workflow

1. Run `python tools/chapter_alignment_audit.py`.
2. Review `REVIEW_QUEUE/COMPLETED/slidedeck_alignment_report.md` for low-coverage chapters.
3. For each flagged chapter, add or revise:
   - one discussion prompt, and
   - one action commitment statement.
4. Re-run the audit and confirm improvements.

