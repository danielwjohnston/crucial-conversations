# Slidedeck Alignment Report

This report compares each chapter deck to its source `.txt` material in `original_files/` 
and uses chapter 10 (`Retake Your Pen`) as a thematic benchmark for action-oriented facilitation.

## Summary table

| Chapter | Source words | Deck words | Slides | Keyword coverage | Discussion prompt | Action prompt |
|---|---:|---:|---:|---:|---|---|
| 1 | 5069 | 311 | 7 | 46.9% | ✅ | ✅ |
| 2 | 3764 | 493 | 8 | 40.6% | ✅ | ✅ |
| 3 | 5404 | 412 | 7 | 58.8% | ⚠️ | ✅ |
| 4 | 9468 | 605 | 10 | 46.4% | ✅ | ✅ |
| 5 | 4791 | 557 | 8 | 68.8% | ⚠️ | ✅ |
| 6 | 5608 | 431 | 7 | 55.6% | ⚠️ | ✅ |
| 7 | 9025 | 524 | 7 | 76.7% | ⚠️ | ✅ |
| 8 | 7227 | 653 | 10 | 62.1% | ✅ | ✅ |
| 9 | 7338 | 543 | 7 | 57.1% | ✅ | ✅ |
| 10 | 4525 | 537 | 7 | 55.0% | ⚠️ | ✅ |
| 11 | 4059 | 411 | 7 | 61.3% | ⚠️ | ✅ |
| 12 | 2111 | 495 | 7 | 62.1% | ⚠️ | ✅ |
| 13 | 3522 | 582 | 7 | 76.7% | ✅ | ✅ |

## Follow-up focus areas

- Chapter 1 (`chapter_01_crucial_conversation.html`) has lower coverage (46.9%). Candidate missing terms: academy, being, don't, effectively, first, hold, issues, it's, less, life.
- Chapter 2 (`chapter_02_mastering_conversations.html`) has lower coverage (40.6%). Candidate missing terms: academy, being, between, choice, decision, don't, feedback, first, it's, kevin.
- Chapter 3 (`chapter_03_choose_topic.html`) has lower coverage (58.8%). Candidate missing terms: academy, being, don't, feedback, know, like, people, process, safety, sandrine.
- Chapter 4 (`chapter_04_start_heart.html`) has lower coverage (46.4%). Candidate missing terms: academy, behavior, being, don't, feedback, feel, like, look, maria, safety.
- Chapter 5 (`chapter_05_master_stories.html`) has lower coverage (68.8%). Candidate missing terms: academy, clever, feedback, like, person, really, safety, side, students, worth.
- Chapter 6 (`chapter_06_learn_to_look.html`) has lower coverage (55.6%). Candidate missing terms: academy, being, feedback, it's, like, meaning, real, students, take, things.
- Chapter 8 (`chapter_08_state_path.html`) has lower coverage (62.1%). Candidate missing terms: academy, anita, being, feedback, it's, side, skills, students, want, worth.
- Chapter 9 (`chapter_09_explore_paths.html`) has lower coverage (57.1%). Candidate missing terms: academy, agree, being, feedback, meaning, person, person's, side, students, want.
- Chapter 10 (`chapter_10_retake_pen.html`) has lower coverage (55.0%). Candidate missing terms: academy, don't, need, number, safety, side, students, work, worth.
- Chapter 11 (`chapter_11_move_action.html`) has lower coverage (61.3%). Candidate missing terms: academy, being, feedback, like, look, make, safety, side, students, want.
- Chapter 12 (`chapter_12_yeah_but.html`) has lower coverage (62.1%). Candidate missing terms: academy, being, even, feedback, help, side, students, trust, you'll, you're.

- Chapters missing explicit discussion language: 3, 5, 6, 7, 10, 11, 12.
- Chapters missing explicit action language: None.

## Regeneration

Run `python tools/chapter_alignment_audit.py` after revising chapter content to refresh this report.
