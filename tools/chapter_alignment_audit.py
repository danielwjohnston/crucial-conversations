#!/usr/bin/env python3
"""Audit chapter slidedecks against source text files.

This script creates a lightweight alignment report so facilitators can quickly
see whether each chapter deck appears to cover the source text's core terms,
contains discussion prompts, and preserves a cohesive presentation structure.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from html import unescape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_FILES = REPO_ROOT / "original_files"
SLIDEDECKS = REPO_ROOT / "slidedecks"
REPORT_PATH = REPO_ROOT / "REVIEW_QUEUE" / "COMPLETED" / "slidedeck_alignment_report.md"

CHAPTER_MAP = {
    1: ("04 1 What’s a Crucial Conversation.txt", "chapter_01_crucial_conversation.html"),
    2: ("05 2 Mastering Crucial Conversations.txt", "chapter_02_mastering_conversations.html"),
    3: ("07 3 Choose Your Topic.txt", "chapter_03_choose_topic.html"),
    4: ("08 4 Start with Heart.txt", "chapter_04_start_heart.html"),
    5: ("09 5 Master My Stories.txt", "chapter_05_master_stories.html"),
    6: ("11 6 Learn to Look.txt", "chapter_06_learn_to_look.html"),
    7: ("12 7 Make It Safe.txt", "chapter_07_make_safe.html"),
    8: ("13 8 STATE My Path.txt", "chapter_08_state_path.html"),
    9: ("14 9 Explore Others’ Paths.txt", "chapter_09_explore_paths.html"),
    10: ("15 10 Retake Your Pen.txt", "chapter_10_retake_pen.html"),
    11: ("17 11 Move to Action.txt", "chapter_11_move_action.html"),
    12: ("18 12 Yeah, But.txt", "chapter_12_yeah_but.html"),
    13: ("19 13 Putting It All Together.txt", "chapter_13_putting_together.html"),
}

STOP_WORDS = {
    "the", "and", "that", "this", "with", "from", "have", "your", "you", "for", "are", "not", "but", "can",
    "our", "their", "they", "was", "were", "will", "all", "about", "what", "when", "into", "just", "than",
    "then", "them", "how", "why", "who", "where", "which", "while", "been", "also", "more", "most", "much",
    "some", "many", "each", "other", "there", "these", "those", "such", "only", "very", "does", "did", "doing",
    "through", "because", "would", "could", "should", "chapter", "conversation", "conversations",
}


@dataclass
class ChapterAudit:
    chapter: int
    source_file: str
    deck_file: str
    source_words: int
    deck_words: int
    keyword_coverage: float
    missing_keywords: list[str]
    has_discussion_prompt: bool
    has_action_prompt: bool
    slide_count: int


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z']+", text.lower())


def extract_visible_text(html: str) -> str:
    html = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.IGNORECASE)
    html = re.sub(r"<style[\s\S]*?</style>", " ", html, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def top_keywords(text: str, count: int = 15) -> list[str]:
    words = [w for w in tokenize(text) if len(w) > 3 and w not in STOP_WORDS]
    ranked = Counter(words).most_common(count * 3)
    deduped: list[str] = []
    for word, _ in ranked:
        if word not in deduped:
            deduped.append(word)
        if len(deduped) >= count:
            break
    return deduped


def audit_chapter(chapter: int, source_name: str, deck_name: str, baseline: set[str]) -> ChapterAudit:
    source_text = (ORIGINAL_FILES / source_name).read_text(encoding="utf-8", errors="ignore")
    deck_html = (SLIDEDECKS / deck_name).read_text(encoding="utf-8", errors="ignore")
    deck_text = extract_visible_text(deck_html)

    source_tokens = tokenize(source_text)
    deck_tokens = tokenize(deck_text)

    chapter_keywords = set(top_keywords(source_text, count=20))
    baseline_union = chapter_keywords | baseline

    covered = {k for k in baseline_union if k in deck_text.lower()}
    missing = sorted([k for k in baseline_union if k not in covered])

    has_discussion_prompt = bool(re.search(r"discussion|reflect|debrief|pair share", deck_text, flags=re.IGNORECASE))
    has_action_prompt = bool(re.search(r"action|commit|next step|practice", deck_text, flags=re.IGNORECASE))
    slide_count = len(re.findall(r'class="slide[\s"]', deck_html))

    return ChapterAudit(
        chapter=chapter,
        source_file=source_name,
        deck_file=deck_name,
        source_words=len(source_tokens),
        deck_words=len(deck_tokens),
        keyword_coverage=(len(covered) / max(len(baseline_union), 1)) * 100,
        missing_keywords=missing[:10],
        has_discussion_prompt=has_discussion_prompt,
        has_action_prompt=has_action_prompt,
        slide_count=slide_count,
    )


def main() -> None:
    baseline_source = (ORIGINAL_FILES / CHAPTER_MAP[10][0]).read_text(encoding="utf-8", errors="ignore")
    baseline_keywords = set(top_keywords(baseline_source, count=15))

    audits: list[ChapterAudit] = []
    for chapter, (source_name, deck_name) in CHAPTER_MAP.items():
        audits.append(audit_chapter(chapter, source_name, deck_name, baseline_keywords))

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Slidedeck Alignment Report",
        "",
        "This report compares each chapter deck to its source `.txt` material in `original_files/` ",
        "and uses chapter 10 (`Retake Your Pen`) as a thematic benchmark for action-oriented facilitation.",
        "",
        "## Summary table",
        "",
        "| Chapter | Source words | Deck words | Slides | Keyword coverage | Discussion prompt | Action prompt |",
        "|---|---:|---:|---:|---:|---|---|",
    ]

    for a in audits:
        lines.append(
            f"| {a.chapter} | {a.source_words} | {a.deck_words} | {a.slide_count} | "
            f"{a.keyword_coverage:.1f}% | {'✅' if a.has_discussion_prompt else '⚠️'} | {'✅' if a.has_action_prompt else '⚠️'} |"
        )

    lines.extend([
        "",
        "## Follow-up focus areas",
        "",
    ])

    low_coverage = [a for a in audits if a.keyword_coverage < 70]
    if not low_coverage:
        lines.append("- All chapters exceeded the 70% keyword coverage heuristic.")
    else:
        for a in low_coverage:
            lines.append(
                f"- Chapter {a.chapter} (`{a.deck_file}`) has lower coverage ({a.keyword_coverage:.1f}%). "
                f"Candidate missing terms: {', '.join(a.missing_keywords)}."
            )

    no_discussion = [a.chapter for a in audits if not a.has_discussion_prompt]
    no_action = [a.chapter for a in audits if not a.has_action_prompt]

    lines.append("")
    lines.append(f"- Chapters missing explicit discussion language: {', '.join(map(str, no_discussion)) if no_discussion else 'None' }.")
    lines.append(f"- Chapters missing explicit action language: {', '.join(map(str, no_action)) if no_action else 'None' }.")
    lines.append("")
    lines.append("## Regeneration")
    lines.append("")
    lines.append("Run `python tools/chapter_alignment_audit.py` after revising chapter content to refresh this report.")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
