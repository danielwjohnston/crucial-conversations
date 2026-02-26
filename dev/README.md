# Dev Branch — Shared JS Extraction

## Purpose

This folder contains a **development branch** for extracting the shared JavaScript engine from all 13 slidedecks into a single `shared.js` file. This is a non-destructive staging area — production slidedecks in `../slidedecks/` are untouched.

## Problem

Every slidedeck carries ~280 lines of identical inline JavaScript:

- CHAPTERS array + PART_LABELS
- Dropdown builder (`buildDropdown`, `toggleDropdown`, `openDropdown`, `closeDropdown`)
- Slide navigation (`showSlide`, `nextSlide`, `previousSlide`)
- Auto-advance timer (countdown, circle, announcements)
- Keyboard navigation (arrows, home/end, escape, digest keys)
- Digest modals (`openDigest`, `closeDigest`, `closeAllDigests`)
- Deep linking (`handleURLParams`)
- Term tooltips

The only per-chapter differences are:

- `CURRENT_CHAPTER_INDEX` (integer 0–12)
- `DURATIONS_SECONDS` (array of slide timings)

## Solution

Extract all shared logic into `shared.js`. Each chapter HTML only needs:

```html
<script>
    const CURRENT_CHAPTER_INDEX = 11;
    const DURATIONS_SECONDS = [30, 90, 150, 150, 300, 120, 120, 300, 90, 120, 60];
</script>
<script src="shared.js"></script>
```

## Files in this folder

- `shared.js` — The extracted shared engine
- `shared.css` — Symlink/copy of production `../slidedecks/shared.css` for testing
- `test_chapter_12.html` — Copy of Ch 12 modified to use `shared.js` instead of inline JS
- `checklist.md` — Promotion checklist for moving to production

## How to test

1. Open `dev/test_chapter_12.html` in a browser
2. Verify all functionality:
   - [ ] Slides advance with arrow keys and buttons
   - [ ] Chapter dropdown opens and navigates
   - [ ] Auto-advance timer works (press 'A')
   - [ ] Digest modals open/close (press 'D' on discussion slides)
   - [ ] Deep linking works (`?slide=5`, `?slide=last`)
   - [ ] Term tooltips appear on hover/focus
   - [ ] Previous/next chapter boundary navigation works
   - [ ] Keyboard shortcuts: Escape, Home, End
   - [ ] Mobile responsive layout
3. Compare behavior side-by-side with `../slidedecks/chapter_12_yeah_but.html`

## Promotion to production

Once testing passes, follow `checklist.md` to roll out to all 13 chapters.
