#!/usr/bin/env python3
"""
Comprehensive slidedeck rebuild script.

For chapters 5-11 (have original HTML slideshows):
  - Copies rich content from originals
  - Injects modern nav (dropdown, CHAPTERS array, cross-chapter nav, deep linking)
  - Restructures HTML to match gold-standard layout

For chapters 2-4, 12-13 (no original HTML):
  - Fixes broken HTML structure (duplicate main, stray auto-advance, etc.)
  - Removes prev/next chapter buttons
  - Sets totalSlides = slides.length

For chapter 1:
  - Removes prev/next chapter buttons only

Does NOT touch any files in original_files/.
"""

import pathlib
import re
import copy

ROOT = pathlib.Path('/Users/dwjohnston/Library/CloudStorage/OneDrive-TEGNA/Desktop/Crucial Conversations')
SLIDEDECKS = ROOT / 'slidedecks'
ORIGINALS = ROOT / 'original_files'

# ── Mapping: chapter number → (original filename, slidedeck filename) ──
ORIG_MAP = {
    5:  ('chapter5_slideshow.html',       'chapter_05_master_stories.html'),
    6:  ('chapter6_slideshow.html',       'chapter_06_learn_to_look.html'),
    7:  ('chapter7_slideshow.html',       'chapter_07_make_safe.html'),
    8:  ('chapter_8_state_my_path.html',  'chapter_08_state_path.html'),
    9:  ('chapter9_slideshow.html',       'chapter_09_explore_paths.html'),
    10: ('chapter10_slideshow.html',      'chapter_10_retake_pen.html'),
    11: ('chapter11_slideshow.html',      'chapter_11_move_action.html'),
}

# ── Chapter metadata ──
CHAPTERS_META = [
    (1,  'chapter_01_crucial_conversation.html',  "What\u2019s a Crucial Conversation", "And who cares?", 1),
    (2,  'chapter_02_mastering_conversations.html', "Mastering Crucial Conversations", "The power of dialogue", 1),
    (3,  'chapter_03_choose_topic.html',          "Choose Your Topic", "How to be sure you hold the right conversation", 1),
    (4,  'chapter_04_start_heart.html',           "Start with Heart", "How to stay focused on what you really want", 1),
    (5,  'chapter_05_master_stories.html',        "Master My Stories", "How to stay in dialogue when you\u2019re angry, scared, or hurt", 2),
    (6,  'chapter_06_learn_to_look.html',         "Learn to Look", "How to notice when safety is at risk", 2),
    (7,  'chapter_07_make_safe.html',             "Make It Safe", "How to make it safe to talk about almost anything", 2),
    (8,  'chapter_08_state_path.html',            "STATE My Path", "How to speak persuasively, not abrasively", 2),
    (9,  'chapter_09_explore_paths.html',         "Explore Others\u2019 Paths", "How to listen when others blow up or clam up", 2),
    (10, 'chapter_10_retake_pen.html',            "Retake Your Pen", "How to be resilient and hear almost anything", 2),
    (11, 'chapter_11_move_action.html',           "Move to Action", "How to turn crucial conversations into action and results", 3),
    (12, 'chapter_12_yeah_but.html',              "Yeah, But", "Advice for tough cases", 3),
    (13, 'chapter_13_putting_together.html',      "Putting It All Together", "Tools for preparing and learning", 3),
]

def get_prefetch_links(ch_num):
    """Generate prefetch <link> tags for adjacent chapters."""
    lines = []
    for num, fname, *_ in CHAPTERS_META:
        if num == ch_num - 1 or num == ch_num + 1:
            lines.append(f'    <link rel="prefetch" href="{fname}">')
    return '\n'.join(lines)

def get_chapters_js_array():
    """Generate the CHAPTERS JS constant."""
    items = []
    for num, fname, title, subtitle, part in CHAPTERS_META:
        t = title.replace("'", "\\'")
        s = subtitle.replace("'", "\\'")
        items.append(f"            {{ num: {num}, file: '{fname}', title: '{t}', subtitle: '{s}', part: {part} }}")
    return "const CHAPTERS = [\n" + ",\n".join(items) + "\n        ];"

# ── CSS to inject into originals (dropdown + modern header) ──
DROPDOWN_CSS = """
        /* === Modern Header === */
        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 15px 30px;
            border-bottom: 1px solid #ddd;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
            color: #666;
            z-index: 1000;
        }
        .header-brand { }
        .header-slide-counter {
            background: #333;
            color: white;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 13px;
        }

        /* === Persistent Header with Dropdown === */
        .persistent-header {
            position: fixed;
            top: 60px;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #e30613 0%, #c20510 100%);
            color: white;
            padding: 10px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            z-index: 500;
            opacity: 0;
            transform: translateY(-100%);
            transition: all 0.6s ease-in-out;
        }
        .persistent-header.show {
            opacity: 1;
            transform: translateY(0);
        }
        .persistent-header-left {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .persistent-header-title {
            font-size: 0.95em;
            font-weight: bold;
            text-transform: uppercase;
        }
        .persistent-header-subtitle {
            font-size: 0.8em;
            opacity: 0.9;
            font-style: italic;
        }

        /* === Chapter Dropdown === */
        .chapter-dropdown-wrapper {
            position: relative;
        }
        .chapter-dropdown-btn {
            background: rgba(255,255,255,0.15);
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
            padding: 6px 14px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            font-weight: bold;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .chapter-dropdown-btn:hover {
            background: rgba(255,255,255,0.25);
        }
        .chapter-dropdown-btn .arrow {
            font-size: 10px;
            transition: transform 0.2s;
        }
        .chapter-dropdown-btn[aria-expanded="true"] .arrow {
            transform: rotate(180deg);
        }
        .chapter-dropdown-menu {
            display: none;
            position: absolute;
            top: 100%;
            right: 0;
            background: white;
            border-radius: 8px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.2);
            min-width: 320px;
            max-height: 70vh;
            overflow-y: auto;
            z-index: 1000;
            margin-top: 6px;
        }
        .chapter-dropdown-menu.open {
            display: block;
        }
        .dropdown-divider {
            height: 1px;
            background: #eee;
            margin: 4px 0;
        }
        .dropdown-section-label {
            padding: 10px 16px 4px;
            font-size: 11px;
            font-weight: bold;
            text-transform: uppercase;
            color: #999;
            letter-spacing: 0.5px;
        }
        .chapter-dropdown-item {
            display: flex;
            align-items: center;
            padding: 8px 16px;
            cursor: pointer;
            transition: background 0.15s;
            text-decoration: none;
            color: #333;
            font-size: 13px;
            border: none;
            background: none;
            width: 100%;
            text-align: left;
        }
        .chapter-dropdown-item:hover {
            background: #f5f5f5;
        }
        .chapter-dropdown-item.active {
            background: #fef2f2;
            color: #c20510;
            font-weight: bold;
        }
        .ch-num {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            border: 2px solid #ddd;
            font-size: 12px;
            font-weight: bold;
            margin-right: 12px;
            flex-shrink: 0;
        }
        .chapter-dropdown-item.active .ch-num {
            background: #c20510;
            color: white;
            border-color: #c20510;
        }
        .ch-info {
            display: flex;
            flex-direction: column;
            gap: 1px;
        }
        .ch-title {
            font-size: 13px;
        }
        .ch-subtitle {
            font-size: 11px;
            color: #888;
            font-style: italic;
        }
        .chapter-dropdown-item.active .ch-subtitle {
            color: #c20510;
        }

        /* === Footer === */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #e30613;
            color: white;
            padding: 15px 30px;
            text-align: right;
            font-size: 14px;
            z-index: 1000;
        }

        @media (max-width: 768px) {
            .persistent-header { padding: 8px 12px; }
            .persistent-header-title { font-size: 0.8em; }
            .persistent-header-subtitle { display: none; }
            .chapter-dropdown-btn { padding: 4px 10px; font-size: 12px; }
            .chapter-dropdown-menu { min-width: 280px; right: -10px; }
        }
"""

# ── JS to inject (dropdown builder + cross-chapter nav + deep linking) ──
def get_nav_js(ch_idx):
    return f"""
        // ============================================================
        // CHAPTER DATA — single source of truth
        // ============================================================
        {get_chapters_js_array()}

        const PART_LABELS = {{
            1: "Part I \\u2014 Before You Open Your Mouth",
            2: "Part II \\u2014 How to Open Your Mouth",
            3: "Part III \\u2014 How to Finish"
        }};

        const CURRENT_CHAPTER_INDEX = {ch_idx};

        // ============================================================
        // CHAPTER DROPDOWN
        // ============================================================
        function buildDropdown() {{
            const menu = document.getElementById('dropdownMenu');
            menu.innerHTML = '';
            let currentPart = 0;
            CHAPTERS.forEach((ch, idx) => {{
                if (ch.part !== currentPart) {{
                    currentPart = ch.part;
                    if (idx > 0) {{
                        const divider = document.createElement('div');
                        divider.className = 'dropdown-divider';
                        menu.appendChild(divider);
                    }}
                    const label = document.createElement('div');
                    label.className = 'dropdown-section-label';
                    label.textContent = PART_LABELS[currentPart];
                    menu.appendChild(label);
                }}
                const item = document.createElement('div');
                item.className = 'chapter-dropdown-item' + (idx === CURRENT_CHAPTER_INDEX ? ' active' : '');
                item.setAttribute('role', 'menuitem');
                item.setAttribute('tabindex', '0');
                item.innerHTML = `
                    <span class="ch-num">${{ch.num}}</span>
                    <span class="ch-info">
                        <span class="ch-title">${{ch.title}}</span>
                        <span class="ch-subtitle">${{ch.subtitle}}</span>
                    </span>
                `;
                item.addEventListener('click', (e) => {{ e.preventDefault(); e.stopPropagation(); closeDropdown(); if (idx !== CURRENT_CHAPTER_INDEX) window.location.href = ch.file; }});
                item.addEventListener('keydown', (e) => {{ if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); closeDropdown(); if (idx !== CURRENT_CHAPTER_INDEX) window.location.href = ch.file; }} }});
                menu.appendChild(item);
            }});
            const divider = document.createElement('div');
            divider.className = 'dropdown-divider';
            menu.appendChild(divider);
            const backItem = document.createElement('div');
            backItem.className = 'chapter-dropdown-item';
            backItem.setAttribute('role', 'menuitem');
            backItem.setAttribute('tabindex', '0');
            backItem.innerHTML = `<span class="ch-num" style="background:#333;color:white;border-color:#333;">\\u2630</span><span class="ch-info"><span class="ch-title">Back to Chapter Select</span></span>`;
            backItem.addEventListener('click', (e) => {{ e.preventDefault(); e.stopPropagation(); window.location.href = '../index.html'; }});
            backItem.addEventListener('keydown', (e) => {{ if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); window.location.href = '../index.html'; }} }});
            menu.appendChild(backItem);
        }}

        const dropdownBtn = document.getElementById('dropdownBtn');
        const dropdownMenu = document.getElementById('dropdownMenu');

        function toggleDropdown() {{
            const isOpen = dropdownMenu.classList.contains('open');
            if (isOpen) closeDropdown(); else openDropdown();
        }}
        function openDropdown() {{
            dropdownMenu.classList.add('open');
            dropdownBtn.classList.add('open');
            dropdownBtn.setAttribute('aria-expanded', 'true');
        }}
        function closeDropdown() {{
            dropdownMenu.classList.remove('open');
            dropdownBtn.classList.remove('open');
            dropdownBtn.setAttribute('aria-expanded', 'false');
        }}
        dropdownBtn.addEventListener('click', toggleDropdown);
        document.addEventListener('click', (e) => {{
            if (!e.target.closest('.chapter-dropdown-wrapper')) closeDropdown();
        }});

        // ============================================================
        // CROSS-CHAPTER NAVIGATION
        // ============================================================
        function goToNextChapter() {{
            if (CURRENT_CHAPTER_INDEX < CHAPTERS.length - 1) {{
                window.location.href = CHAPTERS[CURRENT_CHAPTER_INDEX + 1].file;
            }}
        }}
        function goToPrevChapter() {{
            if (CURRENT_CHAPTER_INDEX > 0) {{
                window.location.href = CHAPTERS[CURRENT_CHAPTER_INDEX - 1].file + '?slide=last';
            }} else {{
                window.location.href = '../index.html';
            }}
        }}
"""


def get_modern_showslide_and_nav():
    """Returns JS for showSlide with clamping, boundary-aware next/prev, keyboard handler, deep linking."""
    return """
        function showSlide(n) {
            slides[currentSlide].classList.remove('active');
            slides[currentSlide].classList.remove('with-header');
            slides[currentSlide].removeAttribute('tabindex');

            currentSlide = Math.max(0, Math.min(n, totalSlides - 1));
            slides[currentSlide].classList.add('active');

            if (currentSlide === 0) {
                chapterHeader.classList.remove('show');
            } else {
                chapterHeader.classList.add('show');
                slides[currentSlide].classList.add('with-header');
            }

            document.getElementById('slideNumber').textContent = currentSlide + 1;

            slides[currentSlide].setAttribute('tabindex', '-1');
            slides[currentSlide].focus();

            if (autoAdvanceEnabled) {
                startTimer();
            }
        }

        function nextSlide() {
            if (currentSlide < totalSlides - 1) {
                showSlide(currentSlide + 1);
            } else if (CURRENT_CHAPTER_INDEX < CHAPTERS.length - 1) {
                window.location.href = CHAPTERS[CURRENT_CHAPTER_INDEX + 1].file;
            }
        }

        function previousSlide() {
            if (currentSlide > 0) {
                showSlide(currentSlide - 1);
            } else if (CURRENT_CHAPTER_INDEX > 0) {
                window.location.href = CHAPTERS[CURRENT_CHAPTER_INDEX - 1].file + '?slide=last';
            }
        }

        document.addEventListener('keydown', function(event) {
            if (event.target.closest('.chapter-dropdown-menu')) return;
            const anyDigestOpen = !!document.querySelector('.digest-modal.active');

            if (event.key === 'Escape') {
                if (anyDigestOpen) { closeAllDigests(); } else { closeDropdown(); }
                return;
            }
            if (event.key === 'ArrowLeft') {
                if (anyDigestOpen) closeAllDigests();
                previousSlide();
            } else if (event.key === 'ArrowRight') {
                if (anyDigestOpen) closeAllDigests();
                nextSlide();
            } else if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
                if (anyDigestOpen) { closeAllDigests(); return; }
                const activeSlide = document.querySelector('.slide.active');
                const digestBtn = activeSlide?.querySelector('.digest-pill[data-digest], .digest-btn');
                if (digestBtn) {
                    const digestId = digestBtn.getAttribute('data-digest') || digestBtn.getAttribute('onclick')?.match(/\\d+/)?.[0];
                    if (digestId) openDigest(Number(digestId));
                }
            } else if (event.key === 'a' || event.key === 'A') {
                toggleAutoAdvance();
            } else if (event.key === 'd' || event.key === 'D') {
                if (anyDigestOpen) { closeAllDigests(); return; }
                const activeSlide = document.querySelector('.slide.active');
                const digestBtn = activeSlide?.querySelector('.digest-pill[data-digest], .digest-btn');
                if (digestBtn) {
                    const digestId = digestBtn.getAttribute('data-digest') || digestBtn.getAttribute('onclick')?.match(/\\d+/)?.[0];
                    if (digestId) openDigest(Number(digestId));
                }
            }
        });

        // ============================================================
        // DEEP LINKING — ?slide=X or ?slide=last
        // ============================================================
        function handleURLParams() {
            const params = new URLSearchParams(window.location.search);
            const sl = params.get('slide');
            if (sl === 'last') { showSlide(totalSlides - 1); return true; }
            else if (sl) {
                const slideIdx = parseInt(sl) - 1;
                if (slideIdx >= 0 && slideIdx < totalSlides) { showSlide(slideIdx); return true; }
            }
            return false;
        }

        // ============================================================
        // INIT
        // ============================================================
        buildDropdown();
        if (!handleURLParams()) { showSlide(0); }
"""


def get_persistent_header_html(ch_num, title, subtitle):
    """Generate the persistent header HTML with dropdown."""
    return f"""        <div class="persistent-header" id="chapterHeader">
            <div class="persistent-header-left">
                <span class="persistent-header-title" id="headerTitle">Ch. {ch_num}: {title.upper()}</span>
                <span class="persistent-header-subtitle" id="headerSubtitle">{subtitle}</span>
            </div>
            <div class="chapter-dropdown-wrapper">
                <button class="chapter-dropdown-btn" id="dropdownBtn" aria-expanded="false" aria-haspopup="true">
                    Chapters <span class="arrow">&#9660;</span>
                </button>
                <div class="chapter-dropdown-menu" id="dropdownMenu" role="menu">
                </div>
            </div>
        </div>
"""


MODERN_HEADER_HTML = """    <header class="header" role="banner">
        <span class="header-brand">CrucialLearning.com | 800.449.5989</span>
        <span class="header-slide-counter" id="slideCounter">
            <span id="slideNumber">1</span> / <span id="totalSlides">0</span>
        </span>
    </header>
"""

MODERN_FOOTER_HTML = """    <footer class="footer" role="contentinfo">
        &copy;2026 Leadership Development. All rights reserved.
    </footer>
"""

MODERN_NAV_HTML = """    <nav class="navigation" role="navigation" aria-label="Slide navigation">
        <button class="nav-btn" onclick="previousSlide()" aria-label="Previous slide">&larr; Back</button>
        <div class="timer-container" id="timerContainer">
            <div class="circular-timer">
                <svg width="60" height="60">
                    <circle class="timer-background" cx="30" cy="30" r="26"/>
                    <circle class="timer-progress" id="timerCircle" cx="30" cy="30" r="26"/>
                </svg>
                <div class="timer-text" id="timerText">0:00</div>
            </div>
        </div>
        <button class="auto-advance-toggle" onclick="toggleAutoAdvance()" aria-pressed="false">
            <span aria-hidden="true">&#9654;</span> Auto-Advance: OFF
        </button>
        <button class="nav-btn" onclick="nextSlide()" aria-label="Next slide">Next &rarr;</button>
    </nav>
"""


# ═══════════════════════════════════════════════════════════════════════
# PROCESS CHAPTERS WITH ORIGINALS (5-11)
# ═══════════════════════════════════════════════════════════════════════
def process_original_chapter(ch_num, orig_name, deck_name):
    """Rebuild a slidedeck from its original HTML + modern nav features."""
    orig_path = ORIGINALS / orig_name
    deck_path = SLIDEDECKS / deck_name

    if not orig_path.exists():
        print(f"  SKIP ch{ch_num}: original {orig_name} not found")
        return

    text = orig_path.read_text()
    ch_idx = ch_num - 1
    meta = CHAPTERS_META[ch_idx]
    _, _, title, subtitle, part = meta

    # ── 1. Inject dropdown CSS before closing </style> ──
    # First remove any existing .header, .footer CSS that might conflict
    # We'll add our own at the end of the style block
    if '</style>' in text:
        # Remove original header/footer CSS (simple patterns)
        text = re.sub(r'/\*[^*]*Modern Header[^*]*\*/.*?(?=\n\s*/\*|\n\s*</style>)', '', text, flags=re.S)
        text = text.replace('</style>', DROPDOWN_CSS + '\n    </style>', 1)

    # ── 2. Add prefetch links before </head> ──
    prefetch = get_prefetch_links(ch_num)
    text = text.replace('</head>', prefetch + '\n</head>', 1)

    # ── 3. Replace everything between <body> and <main with modern structure ──
    # The originals have: skip-link, header, slide-counter, timerAria, persistent-header, [digest modals], main
    # We need: skip-link, modern header, modern footer, [digest modals], main with timerAria + persistent-header

    # Extract digest modals (they're between persistent-header and main)
    digest_modals = ''
    digest_match = re.findall(r'(<div class="digest-modal".*?</div>\s*</div>\s*</div>)', text, re.S)
    if digest_match:
        digest_modals = '\n'.join(digest_match)

    # Extract main content (slides) — handle both <main> and <div class="slideshow-container">
    main_match = re.search(r'<main[^>]*>(.*?)</main>', text, re.S)
    if not main_match:
        # Try div.slideshow-container (ch5, ch6 pattern)
        main_match = re.search(r'<div class="slideshow-container">(.*?)(?=\n\s*<(?:nav|div class="navigation"|footer))', text, re.S)
    if not main_match:
        print(f"  ERROR ch{ch_num}: could not find slide content container")
        return
    raw_content = main_match.group(1).strip()

    # Strip out any slide-counter and persistent-header that were INSIDE the container
    # (we'll add our own persistent-header with dropdown)
    raw_content = re.sub(r'<div class="slide-counter">.*?</div>', '', raw_content, flags=re.S)
    raw_content = re.sub(r'<!--.*?Persistent.*?-->\s*', '', raw_content, flags=re.S)
    # Strip persistent-header (different formats across originals)
    raw_content = re.sub(r'<div class="persistent-header"[^>]*>.*?(?:</div>\s*){1,3}', '', raw_content, count=1, flags=re.S)
    # Also strip timerAria if present inside (we add our own)
    raw_content = re.sub(r'<div id="timerAria"[^>]*>.*?</div>', '', raw_content, flags=re.S)
    slides_content = raw_content.strip()

    # Extract original nav (we'll replace it)
    # Extract script content
    script_match = re.search(r'<script>(.*?)</script>', text, re.S)
    if not script_match:
        print(f"  ERROR ch{ch_num}: could not find <script> content")
        return
    orig_js = script_match.group(1)

    # Extract CSS
    style_match = re.search(r'(<style>.*?</style>)', text, re.S)
    if not style_match:
        print(f"  ERROR ch{ch_num}: could not find <style> content")
        return
    full_css = style_match.group(1)

    # Extract head (everything before </head>)
    head_match = re.search(r'(<!DOCTYPE.*?</head>)', text, re.S)
    if not head_match:
        print(f"  ERROR ch{ch_num}: could not find head section")
        return
    head_section = head_match.group(1)

    # ── 4. Build the new file ──
    persistent_header = get_persistent_header_html(ch_num, title, subtitle)

    # Build body
    body = f"""<body>
    <a class="skip-link" href="#main-content">Skip to content</a>

{MODERN_HEADER_HTML}
{MODERN_FOOTER_HTML}
{('    ' + digest_modals) if digest_modals else ''}

    <main id="main-content" class="slideshow-container" aria-label="Slideshow presentation">
        <div id="timerAria" class="sr-only" aria-live="polite" aria-atomic="true"></div>

{persistent_header}
        {slides_content}
    </main>

{MODERN_NAV_HTML}
    <script>
{get_nav_js(ch_idx)}
"""

    # Now add the original JS but REPLACE certain parts:
    # - Remove old showSlide, nextSlide, previousSlide, keyboard handler
    # - Remove old variable declarations that we'll replace
    # - Keep: DURATIONS_SECONDS, digest functions, timer functions

    # Extract DURATIONS_SECONDS or auto-generate for ~30 min
    dur_match = re.search(r'(const DURATIONS_SECONDS\s*=\s*\[.*?\];)', orig_js, re.S)
    if dur_match:
        durations_js = dur_match.group(1)
        # Check if total exceeds 30 min and normalize
        dur_values = [int(x) for x in re.findall(r'\d+', dur_match.group(1))]
        dur_total = sum(dur_values)
        if dur_total > 2100:  # more than 35 min — scale down to ~30 min
            scale = 1800 / dur_total
            new_values = [max(15, round(v * scale)) for v in dur_values]
            entries = ',\n            '.join(f'{v}' for v in new_values)
            durations_js = f'const DURATIONS_SECONDS = [\n            {entries}\n        ];'
    else:
        # Auto-generate: count actual slides and distribute ~1800s
        actual_slides = len(re.findall(r'<div class="slide[\s"]', slides_content))
        if actual_slides > 0:
            base = 1800 // actual_slides
            rem = 1800 - base * actual_slides
            vals = [base + (1 if i < rem else 0) for i in range(actual_slides)]
            # Title slide gets less time
            if vals:
                vals[0] = min(vals[0], 30)
                leftover = sum(vals) - 1800
                if leftover != 0 and len(vals) > 1:
                    vals[1] = vals[1] - leftover
            entries = ',\n            '.join(f'{v}' for v in vals)
            durations_js = f'const DURATIONS_SECONDS = [\n            {entries}\n        ];'
        else:
            durations_js = 'const DURATIONS_SECONDS = [];'

    # Check if original has digest functions
    has_digest = 'function openDigest' in orig_js
    has_close_all = 'function closeAllDigests' in orig_js

    body += f"""
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        const chapterHeader = document.getElementById('chapterHeader');
        const timerContainer = document.getElementById('timerContainer');
        const timerText = document.getElementById('timerText');
        const timerCircle = document.getElementById('timerCircle');
        const autoAdvanceToggle = document.querySelector('.auto-advance-toggle');
        const timerAria = document.getElementById('timerAria');

        let autoAdvanceEnabled = false;
        let countdownInterval = null;
        let remainingTime = 0;
        let totalDuration = 0;
        let lastAnnouncement = -1;

        document.getElementById('totalSlides').textContent = totalSlides;

        {durations_js}
"""

    # Add digest functions (from original or stubs)
    if has_digest:
        # Extract the actual digest functions from original
        digest_funcs = []
        for func_name in ['openDigest', 'closeDigest', 'closeAllDigests']:
            func_match = re.search(rf'(function {func_name}\(.*?\n\s*\}})', orig_js, re.S)
            if func_match:
                digest_funcs.append('        ' + func_match.group(1))
        if digest_funcs:
            body += '\n'.join(digest_funcs) + '\n'
        # Also add the click-outside-modal handler
        body += """
        document.querySelectorAll('.digest-modal').forEach((modal) => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    const num = modal.id.replace('digestModal', '');
                    closeDigest(num);
                }
            });
        });
"""
    else:
        body += """
        function openDigest(n) {}
        function closeDigest(n) {}
        function closeAllDigests() {}
"""

    # Add timer functions
    body += """
        function getSlideDuration() {
            return DURATIONS_SECONDS[currentSlide] ?? 60;
        }

        function formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            return `${mins}:${secs.toString().padStart(2, '0')}`;
        }

        function updateTimerCircle() {
            const circumference = 163.36;
            const progress = remainingTime / totalDuration;
            const offset = circumference * (1 - progress);
            timerCircle.style.strokeDashoffset = offset;
        }

        function announceTimer(msg) {
            if (timerAria) { timerAria.textContent = msg; }
        }

        function startTimer() {
            if (!autoAdvanceEnabled) return;
            stopTimer();
            totalDuration = getSlideDuration();
            remainingTime = totalDuration;
            lastAnnouncement = -1;
            timerText.textContent = formatTime(remainingTime);
            updateTimerCircle();
            countdownInterval = setInterval(() => {
                remainingTime--;
                timerText.textContent = formatTime(remainingTime);
                updateTimerCircle();
                if (remainingTime % 60 === 0 || (remainingTime < 60 && remainingTime % 10 === 0)) {
                    if (remainingTime !== lastAnnouncement) {
                        announceTimer(`${formatTime(remainingTime)} remaining`);
                        lastAnnouncement = remainingTime;
                    }
                }
                if (remainingTime <= 0) { stopTimer(); nextSlide(); }
            }, 1000);
        }

        function stopTimer() {
            if (countdownInterval) { clearInterval(countdownInterval); countdownInterval = null; }
        }

        function toggleAutoAdvance() {
            autoAdvanceEnabled = !autoAdvanceEnabled;
            if (autoAdvanceEnabled) {
                autoAdvanceToggle.innerHTML = '<span aria-hidden="true">⏸</span> Auto-Advance: ON';
                autoAdvanceToggle.setAttribute('aria-pressed', 'true');
                autoAdvanceToggle.classList.add('active');
                timerContainer.classList.add('active');
                startTimer();
            } else {
                autoAdvanceToggle.innerHTML = '<span aria-hidden="true">▶</span> Auto-Advance: OFF';
                autoAdvanceToggle.setAttribute('aria-pressed', 'false');
                autoAdvanceToggle.classList.remove('active');
                timerContainer.classList.remove('active');
                stopTimer();
            }
        }
"""

    # Add modern showSlide + navigation + keyboard handler + deep linking
    body += get_modern_showslide_and_nav()

    body += """
    </script>
</body>
</html>
"""

    # Write the final file
    final = head_section + '\n' + body
    deck_path.write_text(final)
    slide_count = len(re.findall(r'<div class="slide[\s"]', final))
    dur_sum = sum(int(x) for x in re.findall(r'\d+', durations_js))
    print(f"  OK ch{ch_num}: {slide_count} slides, {dur_sum}s ({dur_sum/60:.1f} min)")


# ═══════════════════════════════════════════════════════════════════════
# PROCESS CHAPTERS WITHOUT ORIGINALS (structural fix only)
# ═══════════════════════════════════════════════════════════════════════
def fix_structural_issues(ch_num, deck_name):
    """Fix broken HTML structure in chapters without originals."""
    deck_path = SLIDEDECKS / deck_name
    if not deck_path.exists():
        print(f"  SKIP ch{ch_num}: {deck_name} not found")
        return

    text = deck_path.read_text()
    ch_idx = ch_num - 1
    meta = CHAPTERS_META[ch_idx]
    _, _, title, subtitle, part = meta

    # ── 1. Remove prev/next chapter buttons from nav ──
    text = re.sub(r'\s*<button[^>]*class="nav-btn chapter-nav-btn"[^>]*>.*?</button>', '', text, flags=re.S)

    # ── 2. Fix the broken double-main structure (ch2-13) ──
    # Pattern: first <main> with stray content, then </header>, then persistent-header, then second <main>
    broken_pattern = re.compile(
        r'<main id="main-content"[^>]*aria-label="Slideshow presentation">\s*'
        r'<div class="slide title-slide">\s*<span id="currentSlide">.*?</span>.*?</div>\s*'
        r'<div>.*?</div>\s*'
        r'<button class="auto-advance-toggle"[^>]*>.*?</button>\s*'
        r'</header>\s*'
        r'(<div class="persistent-header".*?</div>\s*</div>\s*</div>)\s*'
        r'<main class="slideshow-container" id="main-content">',
        re.S
    )
    m = broken_pattern.search(text)
    if m:
        persistent_header_html = m.group(1)
        replacement = (
            '<main id="main-content" class="slideshow-container" aria-label="Slideshow presentation">\n'
            '        <div id="timerAria" class="sr-only" aria-live="polite" aria-atomic="true"></div>\n\n'
            f'        {persistent_header_html}\n'
        )
        text = broken_pattern.sub(replacement, text, count=1)

    # ── 3. Ensure first slide has title-slide class ──
    text = re.sub(
        r'<div class="slide active">',
        '<div class="slide active title-slide">',
        text, count=1
    )

    # ── 4. Add brand-logo if missing ──
    first_slide_match = re.search(r'<div class="slide active title-slide">\s*\n', text)
    if first_slide_match and '<div class="brand-logo">' not in text[first_slide_match.start():first_slide_match.start()+300]:
        text = text.replace(
            '<div class="slide active title-slide">\n',
            '<div class="slide active title-slide">\n            <div class="brand-logo">Leadership Bookclub</div>\n',
            1
        )

    # ── 5. Fix totalSlides to be dynamic ──
    text = re.sub(r'const totalSlides = \d+;', 'const totalSlides = slides.length;', text, count=1)

    # ── 6. Ensure totalDuration and lastAnnouncement exist ──
    if 'let totalDuration' not in text:
        text = text.replace(
            'let remainingTime = 0;',
            'let remainingTime = 0;\n        let totalDuration = 0;\n        let lastAnnouncement = -1;',
            1
        )

    deck_path.write_text(text)
    slide_count = len(re.findall(r'<div class="slide[\s"]', text))
    dur_match = re.search(r'DURATIONS_SECONDS\s*=\s*\[(.*?)\]', text, re.S)
    dur_sum = sum(int(x) for x in re.findall(r'\d+', dur_match.group(1))) if dur_match else 0
    print(f"  OK ch{ch_num}: {slide_count} slides, {dur_sum}s ({dur_sum/60:.1f} min) [structural fix]")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════
def main():
    print("=== Rebuilding slidedecks ===\n")

    # Chapter 1: just remove prev/next ch buttons
    print("Chapter 1: removing prev/next ch buttons")
    ch1_path = SLIDEDECKS / 'chapter_01_crucial_conversation.html'
    if ch1_path.exists():
        text = ch1_path.read_text()
        text = re.sub(r'\s*<button[^>]*class="nav-btn chapter-nav-btn"[^>]*>.*?</button>', '', text, flags=re.S)
        ch1_path.write_text(text)
        print("  OK ch1: prev/next buttons removed")

    # Chapters 5-11: rebuild from originals
    print("\nChapters 5-11: rebuilding from originals + modern nav")
    for ch_num, (orig_name, deck_name) in sorted(ORIG_MAP.items()):
        print(f"Chapter {ch_num}:")
        process_original_chapter(ch_num, orig_name, deck_name)

    # Chapters 2-4, 12-13: structural fix
    print("\nChapters 2-4, 12-13: structural fixes")
    for ch_num in [2, 3, 4, 12, 13]:
        meta = CHAPTERS_META[ch_num - 1]
        deck_name = meta[1]
        print(f"Chapter {ch_num}:")
        fix_structural_issues(ch_num, deck_name)

    print("\n=== Done ===")


if __name__ == '__main__':
    main()
