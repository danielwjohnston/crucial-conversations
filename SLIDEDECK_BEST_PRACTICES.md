# Slidedeck Best Practices — Leadership Bookclub

> Definitive reference for architecture, UI, content structure, timing, and patterns.
> All styling lives in `slidedecks/shared.css`. Chapters contain only HTML + JS.

---

## 1. Architecture

### File Structure

```
slidedecks/
  shared.css                          ← Single source of truth for ALL styles
  chapter_01_crucial_conversation.html
  chapter_02_mastering_conversations.html
  ...
  chapter_13_putting_together.html
index.html                            ← Landing page / chapter selector
```

### Key Principles

- **Zero inline `<style>` blocks** — every chapter uses `<link rel="stylesheet" href="shared.css">`
- **One CSS file to rule them all** — any style fix applies to all 13 chapters instantly
- **CSS custom properties** define all layout zones; everything else is derived via `calc()`
- **No magic numbers** — spacing is mathematically computed from viewport size

---

## 2. CSS Layout System (`shared.css`)

### Source-of-Truth Variables

All layout spacing is derived from 5 base variables defined in `:root`:

```css
:root {
    /* Fixed element heights — the ONLY numbers you ever change */
    --header-h: 52px;       /* top bar */
    --persistent-h: 48px;   /* red chapter header */
    --nav-h: 50px;          /* navigation button row */
    --footer-h: 50px;       /* bottom red footer */
    --gap: 8px;             /* breathing room between zones */
}
```

### Derived Spacing (never edit these — they auto-calculate)

```css
--top-clear:      calc(var(--header-h) + var(--gap));
--top-clear-full: calc(var(--header-h) + var(--persistent-h) + var(--gap) * 3);
--bottom-clear:   calc(var(--footer-h) + var(--nav-h) + var(--gap) * 3);
--content-h:      calc(100vh - var(--top-clear) - var(--bottom-clear));
--content-h-with-header: calc(100vh - var(--top-clear-full) - var(--bottom-clear));
```

### How Layout Zones Work

```
+─────────────────────────────────────+  0
|  .header  (height: var(--header-h)) |  ← fixed, z-index: 1000
+─────────────────────────────────────+  var(--header-h)
|  --gap--                            |
+─────────────────────────────────────+  var(--top-clear)
|  .persistent-header                 |  ← fixed, z-index: 500 (slides 2+)
|  (height: var(--persistent-h))      |
+─────────────────────────────────────+
|  --gap-- × 2                        |
+═════════════════════════════════════+  var(--top-clear-full)
|                                     |
|  SLIDE CONTENT ZONE                 |  ← scrollable
|  height: var(--content-h-with-header)|
|                                     |
+═════════════════════════════════════+
|  --gap-- × 3                        |
+─────────────────────────────────────+
|  .navigation (height: var(--nav-h)) |  ← fixed
+─────────────────────────────────────+
|  --gap-- × 3                        |
+─────────────────────────────────────+
|  .footer (height: var(--footer-h))  |  ← fixed, z-index: 1000
+─────────────────────────────────────+  100vh
```

### Responsive Breakpoints

At each breakpoint, override **only the 5 base variables** — all `calc()` values update automatically:

```css
@media (max-width: 768px) {
    :root {
        --header-h: 48px;
        --persistent-h: 40px;
        --nav-h: 44px;
        --footer-h: 44px;
    }
}

@media (max-width: 480px) {
    :root {
        --header-h: 44px;
        --persistent-h: 36px;
        --nav-h: 40px;
        --footer-h: 40px;
    }
}
```

### Title Slide Sizing

The title slide fills available space with a 4:3 aspect ratio:

```css
.title-slide {
    width: min(90vw, calc(var(--content-h) * 4 / 3));
    max-width: 1200px;
    height: var(--content-h);
}
```

- Width = the smaller of 90% viewport width or 4:3 ratio based on available height
- Height = exact available content zone
- Result: always fits, maintains proportions, adapts to any screen

---

## 3. Slide Types & Structure

Every chapter follows this ordered structure:

| # | Slide Type | Class(es) | Purpose | Duration |
| --- | --- | --- | --- | --- |
| 1 | **Title** | `.slide.title-slide` | Red gradient, brand logo, chapter #, title, subtitle | 20-45 s |
| 2-N | **Content** | `.slide` | Core chapter material | 60-240 s each |
| - | **Discussion Break #1** | `.slide.discussion-slide` | Single question + digest pill | 240-540 s |
| N+1... | **Content** (cont.) | `.slide` | More chapter material | 60-240 s each |
| - | **Discussion Break #2** | `.slide.discussion-slide` | Single question + digest pill | 240-540 s |
| - | **This Week's Challenge** | `.slide` | Actionable homework | 120-240 s |
| - | **More to Ponder** | `.slide` | 4 reflective prompts, "Choose 1-2" | 120-240 s |
| - | **Look Ahead** | `.slide.look-ahead-slide` | Preview next chapter + optional prep | 60-90 s |

### Key Rules

- **Exactly 2 discussion breaks** placed at natural content breaks (~1/3 and ~2/3 through)
- **~12-16 slides total** per chapter
- **~30 minutes total** target (Ch1 is an exception at ~60 min)
- **No standalone digest slides** — digest content lives in modals

---

## 4. Discussion Break Pattern

```html
<div class="slide discussion-slide">
    <div class="slide-content">
        <h2>Discussion Break #1</h2>
        <div class="discussion-question">
            <p>A single, cohesive discussion question that ties together
            the key concepts from the preceding content slides.</p>
        </div>
        <button class="digest-pill" type="button" data-digest="1"
                onclick="openDigest(1)" aria-haspopup="dialog"
                aria-controls="digestModal1">
            <span class="dot" aria-hidden="true"></span>
            Dan's Digest
        </button>
    </div>
</div>
```

- Blue border/background (`#f0f8ff`, border `#4a90e2`)
- **One single, comprehensive question** per discussion break (not multiple numbered prompts)
- The question should be cohesive and open-ended, inviting whole-group conversation
- **Always whole-group discussion** — never "break into pairs" or "turn to a partner"
- Green digest pill at the bottom (not a separate slide)
- Question should tie together the content slides that preceded the break

---

## 5. Dan's Digest — Modal Pattern

Digest content is **never a separate slide**. It's a modal overlay triggered by the green pill.

```html
<!-- Outside <main>, after </main> and before <nav> -->
<div class="digest-modal" id="digestModal1" role="dialog"
     aria-labelledby="digestTitle1" aria-modal="true">
    <div class="digest-content">
        <button class="digest-close" onclick="closeDigest(1)"
                aria-label="Close">&times;</button>
        <h2 id="digestTitle1">Dan's Digest</h2>
        <div class="digest-answer">
            <h4>Answer Key (Discussion Break #1)</h4>
            <p>Answer content with <strong>bold key terms</strong>.</p>
        </div>
        <div class="digest-insights">
            <h4>Key Points</h4>
            <ul>
                <li>Insight 1</li>
                <li>Insight 2</li>
                <li>Insight 3</li>
            </ul>
        </div>
    </div>
</div>
```

- Green border/background (`#f0fff4`, border `#48bb78`)
- Opened by pill button, closed by X button, Escape key, or clicking backdrop
- Keyboard: D key or Arrow Up/Down opens digest on current slide; Escape closes

---

## 6. "More to Ponder" Slide

```html
<div class="slide">
    <div class="slide-content">
        <h2>More to Ponder</h2>
        <p class="subtitle">Use these as a quick review of key takeaways.</p>
        <div class="story-box">
            <h3>Choose 1-2 prompts</h3>
            <ul>
                <li>Reflective question 1</li>
                <li>Reflective question 2</li>
                <li>Reflective question 3</li>
                <li>Reflective question 4</li>
            </ul>
        </div>
    </div>
</div>
```

- **Not** group discussion — take-home reflection prompts
- 4 bullet prompts, "Choose 1-2" to think about

---

## 7. "Look Ahead" Slide

```html
<div class="slide look-ahead-slide">
    <div class="slide-content">
        <h1>Look Ahead</h1>
        <h2>Chapter N+1: Title</h2>
        <div class="highlight">
            <h3>What we'll focus on next</h3>
            <ul>
                <li>Preview point 1</li>
                <li>Preview point 2</li>
                <li>Preview point 3</li>
            </ul>
        </div>
        <p class="subtitle"><strong>Optional prep:</strong> ...</p>
    </div>
</div>
```

- White background with red border (`.look-ahead-slide`)
- Previews next chapter's topic + optional prep suggestion

---

## 8. Title Slide Pattern

```html
<div class="slide active title-slide">
    <div class="slide-content">
        <div class="brand-logo">Leadership Bookclub</div>
        <h1>CHAPTER N</h1>
        <h2>Chapter Title</h2>
        <p class="subtitle">Subtitle / tagline</p>
    </div>
</div>
```

- Red gradient background, white text, rounded corners
- Sized by CSS variables: fills `var(--content-h)` height, 4:3 width ratio
- Persistent header is **hidden** on slide 1

---

## 9. Content Slide Best Practices

- Use `.highlight` for key points (red left border)
- Use `.story-box` for narrative examples (gray border)
- Use `.bridge-box` for high-impact statements (red gradient, white text)
- Use `.two-column` / `.three-column` grids for comparisons
- Use `.step-box` for sequential processes
- Use `.quote-box` for book quotes
- Use `.column-box` for grid items
- Keep bullet lists to **5 items max** per slide
- Use `<strong>` for emphasis, `<em>` for secondary emphasis
- Every slide should have a clear `<h2>` title

---

## 10. HTML Structure (Full Page)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Leadership Bookclub - Chapter Title</title>
    <link rel="stylesheet" href="shared.css">
    <link rel="prefetch" href="chapter_NN_prev.html">
    <link rel="prefetch" href="chapter_NN_next.html">
</head>
<body>
    <a class="skip-link" href="#main-content">Skip to content</a>
    <header class="header">...</header>
    <footer class="footer">...</footer>

    <main id="main-content" class="slideshow-container">
        <div id="timerAria" class="sr-only" ...></div>
        <div class="persistent-header" id="chapterHeader">...</div>

        <!-- SLIDES -->
        <div class="slide active title-slide">...</div>
        <div class="slide">...</div>
        <div class="slide discussion-slide">...</div>
        ...
    </main>

    <!-- DIGEST MODALS (outside main, before nav) -->
    <div class="digest-modal" id="digestModal1">...</div>
    <div class="digest-modal" id="digestModal2">...</div>

    <nav class="navigation">...</nav>

    <script>/* Chapter JS */</script>
</body>
</html>
```

**Key:** No `<style>` block — only `<link rel="stylesheet" href="shared.css">`.

---

## 11. JavaScript Essentials

Every chapter `<script>` must include:

- `CHAPTERS` array (all 13 chapters, unicode-escaped apostrophes)
- `PART_LABELS` object (3 parts)
- `CURRENT_CHAPTER_INDEX` (0-indexed)
- `buildDropdown()` function
- `showSlide()` with `with-header` class toggle
- `nextSlide()` / `previousSlide()` with cross-chapter boundary navigation
- `openDigest()` / `closeDigest()` / `closeAllDigests()` (functional, not stubs)
- Keyboard handler: Arrow keys, Escape, A (auto-advance), D (digest)
- `handleURLParams()` for deep linking (`?slide=X`, `?slide=last`)
- `DURATIONS_SECONDS` array — **must match slide count exactly**
- Auto-advance timer logic with circular SVG progress

---

## 12. Timing Guidelines

| Slide Type | Typical Duration |
| --- | --- |
| Title | 20-45 seconds |
| Content (light) | 60-90 seconds |
| Content (heavy / exercise) | 120-240 seconds |
| Discussion Break | 240-540 seconds |
| This Week's Challenge | 120-240 seconds |
| More to Ponder | 120-240 seconds |
| Look Ahead | 60-90 seconds |

**Target total: ~30 minutes** (1,800 seconds) per chapter.

---

## 13. Anti-Patterns (Do NOT)

- **Standalone digest slides** — digest content goes in modals, not separate slides
- **More than 2 discussion breaks** — 2 is the max; use "More to Ponder" for extras
- **Multiple numbered prompts** on discussion slides — use one cohesive question
- **"Break into pairs"** — all discussion is whole-group
- **Inline `<style>` blocks** — all CSS lives in `shared.css`
- **Fixed pixel values for layout spacing** — use CSS variables and `calc()`
- **Stray HTML outside slide divs** — all visible content inside `<div class="slide">`
- **Empty function stubs** for digest — must have working `openDigest`/`closeDigest`
- **Giant walls of text** — break into bullets, boxes, columns
- **More than 5 bullets** per list without visual variety

---

*Last updated: Feb 25, 2026*
