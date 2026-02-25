#!/usr/bin/env python3
"""
Propagate chapter navigation system to chapters 2-13.
Chapter 1 is the reference implementation (already updated).
"""
import os
import re

SLIDEDECKS_DIR = "/Users/dwjohnston/Library/CloudStorage/OneDrive-TEGNA/Desktop/Crucial Conversations/slidedecks"

CHAPTERS = [
    {"num": 1,  "file": "chapter_01_crucial_conversation.html",  "title": "What\u2019s a Crucial Conversation", "title_upper": "WHAT\u2019S A CRUCIAL CONVERSATION", "subtitle": "And who cares?"},
    {"num": 2,  "file": "chapter_02_mastering_conversations.html", "title": "Mastering Crucial Conversations", "title_upper": "MASTERING CRUCIAL CONVERSATIONS", "subtitle": "The power of dialogue"},
    {"num": 3,  "file": "chapter_03_choose_topic.html",          "title": "Choose Your Topic", "title_upper": "CHOOSE YOUR TOPIC", "subtitle": "How to be sure you hold the right conversation"},
    {"num": 4,  "file": "chapter_04_start_heart.html",           "title": "Start with Heart", "title_upper": "START WITH HEART", "subtitle": "How to stay focused on what you really want"},
    {"num": 5,  "file": "chapter_05_master_stories.html",        "title": "Master My Stories", "title_upper": "MASTER MY STORIES", "subtitle": "How to stay in dialogue when you\u2019re angry, scared, or hurt"},
    {"num": 6,  "file": "chapter_06_learn_to_look.html",         "title": "Learn to Look", "title_upper": "LEARN TO LOOK", "subtitle": "How to notice when safety is at risk"},
    {"num": 7,  "file": "chapter_07_make_safe.html",             "title": "Make It Safe", "title_upper": "MAKE IT SAFE", "subtitle": "How to make it safe to talk about almost anything"},
    {"num": 8,  "file": "chapter_08_state_path.html",            "title": "STATE My Path", "title_upper": "STATE MY PATH", "subtitle": "How to speak persuasively, not abrasively"},
    {"num": 9,  "file": "chapter_09_explore_paths.html",         "title": "Explore Others\u2019 Paths", "title_upper": "EXPLORE OTHERS\u2019 PATHS", "subtitle": "How to listen when others blow up or clam up"},
    {"num": 10, "file": "chapter_10_retake_pen.html",            "title": "Retake Your Pen", "title_upper": "RETAKE YOUR PEN", "subtitle": "How to be resilient and hear almost anything"},
    {"num": 11, "file": "chapter_11_move_action.html",           "title": "Move to Action", "title_upper": "MOVE TO ACTION", "subtitle": "How to turn crucial conversations into action and results"},
    {"num": 12, "file": "chapter_12_yeah_but.html",              "title": "Yeah, But", "title_upper": "YEAH, BUT", "subtitle": "Advice for tough cases"},
    {"num": 13, "file": "chapter_13_putting_together.html",      "title": "Putting It All Together", "title_upper": "PUTTING IT ALL TOGETHER", "subtitle": "Tools for preparing and learning"},
]

# ============================================================
# CSS TEMPLATES
# ============================================================

OLD_PERSISTENT_CSS = """        .persistent-header {
            position: fixed;
            top: 60px;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #e30613 0%, #c20510 100%);
            color: white;
            padding: 20px 40px;
            text-align: center;
            z-index: 500;
            opacity: 0;
            transform: translateY(-100%);
            transition: all 0.6s ease-in-out;
        }

        .persistent-header.show {
            opacity: 1;
            transform: translateY(0);
        }

        .persistent-header h3 {
            color: white;
            font-size: 0.9em;
            margin-bottom: 5px;
            font-weight: normal;
        }

        .persistent-header h2 {
            color: white;
            font-size: 1.5em;
            margin: 5px 0;
            text-transform: uppercase;
        }

        .persistent-header p {
            color: #f0f0f0;
            font-size: 0.85em;
            margin: 5px 0 0 0;
            font-style: italic;
        }"""

NEW_PERSISTENT_CSS = """        .persistent-header {
            position: fixed;
            top: 60px;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #e30613 0%, #c20510 100%);
            color: white;
            padding: 12px 30px;
            z-index: 500;
            display: flex;
            align-items: center;
            justify-content: space-between;
            opacity: 0;
            transform: translateY(-100%);
            transition: all 0.4s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }

        .persistent-header.show {
            opacity: 1;
            transform: translateY(0);
        }

        .persistent-header-left {
            display: flex;
            align-items: center;
            gap: 16px;
            min-width: 0;
        }

        .persistent-header-title {
            font-size: 1em;
            font-weight: 700;
            letter-spacing: 0.04em;
            white-space: nowrap;
        }

        .persistent-header-subtitle {
            font-size: 0.8em;
            opacity: 0.85;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* === Chapter Dropdown === */
        .chapter-dropdown-wrapper { position: relative; }

        .chapter-dropdown-btn {
            background: rgba(255,255,255,0.15);
            border: 1.5px solid rgba(255,255,255,0.4);
            color: white;
            padding: 6px 14px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
            white-space: nowrap;
        }

        .chapter-dropdown-btn:hover {
            background: rgba(255,255,255,0.25);
            border-color: rgba(255,255,255,0.6);
        }

        .chapter-dropdown-btn .arrow { font-size: 10px; transition: transform 0.2s ease; }
        .chapter-dropdown-btn.open .arrow { transform: rotate(180deg); }

        .chapter-dropdown-menu {
            position: absolute;
            top: calc(100% + 8px);
            right: 0;
            background: white;
            border-radius: 10px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.12);
            min-width: 340px;
            max-height: 70vh;
            overflow-y: auto;
            opacity: 0;
            visibility: hidden;
            transform: translateY(-8px);
            transition: all 0.2s ease;
            z-index: 1100;
            border: 1px solid #ddd;
        }

        .chapter-dropdown-menu.open {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }

        .dropdown-section-label {
            padding: 10px 16px 4px;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #666;
        }

        .dropdown-divider { height: 1px; background: #ddd; margin: 4px 0; }

        .chapter-dropdown-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 16px;
            cursor: pointer;
            transition: background 0.15s ease;
            text-decoration: none;
            color: #333;
        }

        .chapter-dropdown-item:hover { background: #f8f9fa; }
        .chapter-dropdown-item.active { background: #fef2f2; }
        .chapter-dropdown-item.active .ch-num { background: #e30613; color: white; }

        .ch-num {
            width: 28px; height: 28px; border-radius: 50%;
            background: #f8f9fa; color: #444;
            display: flex; align-items: center; justify-content: center;
            font-size: 12px; font-weight: 700; flex-shrink: 0;
            border: 1.5px solid #ddd;
        }

        .ch-info { min-width: 0; }

        .ch-title {
            font-size: 13px; font-weight: 600; color: #333;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: block;
        }

        .ch-subtitle {
            font-size: 11px; color: #666;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: block;
        }"""

CHAPTER_NAV_CSS = """
        /* === Chapter Nav Buttons === */
        .nav-btn.chapter-nav-btn {
            background: #333;
            font-size: 12px;
            padding: 10px 14px;
            width: auto;
            min-width: auto;
        }

        .nav-btn.chapter-nav-btn:hover:not(:disabled) { background: #444; }

        .nav-btn.chapter-nav-btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        @media (max-width: 768px) {
            .persistent-header { padding: 8px 12px; }
            .persistent-header-title { font-size: 0.8em; }
            .persistent-header-subtitle { display: none; }
            .chapter-dropdown-btn { padding: 4px 10px; font-size: 12px; }
            .chapter-dropdown-menu { min-width: 280px; right: -10px; }
            .nav-btn.chapter-nav-btn { display: none; }
        }"""

OLD_HEADER_CSS = """        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 15px 30px;
            border-bottom: 1px solid #ddd;
            font-size: 14px;
            color: #666;
            z-index: 1000;
        }"""

NEW_HEADER_CSS = """        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 0 30px;
            height: 52px;
            border-bottom: 1px solid #ddd;
            font-size: 14px;
            color: #666;
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header-brand {
            font-weight: 600;
            letter-spacing: 0.02em;
        }

        .header-slide-counter {
            background: #333;
            color: white;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            font-variant-numeric: tabular-nums;
        }"""

# ============================================================
# HTML TEMPLATES
# ============================================================

def get_persistent_header_html(ch):
    return f'''    <div class="persistent-header" id="chapterHeader">
            <div class="persistent-header-left">
                <span class="persistent-header-title" id="headerTitle">Ch. {ch["num"]}: {ch["title_upper"]}</span>
                <span class="persistent-header-subtitle" id="headerSubtitle">{ch["subtitle"]}</span>
            </div>
            <div class="chapter-dropdown-wrapper">
                <button class="chapter-dropdown-btn" id="dropdownBtn" aria-expanded="false" aria-haspopup="true">
                    Chapters <span class="arrow">\u25bc</span>
                </button>
                <div class="chapter-dropdown-menu" id="dropdownMenu" role="menu">
                </div>
            </div>
        </div>'''

def get_prefetch_links(idx):
    links = []
    if idx > 0:
        links.append(f'    <link rel="prefetch" href="{CHAPTERS[idx-1]["file"]}">')
    if idx < len(CHAPTERS) - 1:
        links.append(f'    <link rel="prefetch" href="{CHAPTERS[idx+1]["file"]}">')
    return '\n'.join(links)

NEW_HEADER_HTML = '''    <header class="header" role="banner">
        <span class="header-brand">CrucialLearning.com | 800.449.5989</span>
        <span class="header-slide-counter" id="slideCounter">
            <span id="slideNumber">1</span> / <span id="totalSlides">0</span>
        </span>
    </header>'''

# ============================================================
# JS TEMPLATES
# ============================================================

CHAPTERS_JS_BLOCK = '''        // ============================================================
        // CHAPTER DATA \u2014 single source of truth
        // ============================================================
        const CHAPTERS = [
            { num: 1,  file: "chapter_01_crucial_conversation.html",  title: "What\\u2019s a Crucial Conversation", subtitle: "And who cares?", part: 1 },
            { num: 2,  file: "chapter_02_mastering_conversations.html", title: "Mastering Crucial Conversations", subtitle: "The power of dialogue", part: 1 },
            { num: 3,  file: "chapter_03_choose_topic.html",          title: "Choose Your Topic", subtitle: "How to be sure you hold the right conversation", part: 1 },
            { num: 4,  file: "chapter_04_start_heart.html",           title: "Start with Heart", subtitle: "How to stay focused on what you really want", part: 1 },
            { num: 5,  file: "chapter_05_master_stories.html",        title: "Master My Stories", subtitle: "How to stay in dialogue when you\\u2019re angry, scared, or hurt", part: 2 },
            { num: 6,  file: "chapter_06_learn_to_look.html",         title: "Learn to Look", subtitle: "How to notice when safety is at risk", part: 2 },
            { num: 7,  file: "chapter_07_make_safe.html",             title: "Make It Safe", subtitle: "How to make it safe to talk about almost anything", part: 2 },
            { num: 8,  file: "chapter_08_state_path.html",            title: "STATE My Path", subtitle: "How to speak persuasively, not abrasively", part: 2 },
            { num: 9,  file: "chapter_09_explore_paths.html",         title: "Explore Others\\u2019 Paths", subtitle: "How to listen when others blow up or clam up", part: 2 },
            { num: 10, file: "chapter_10_retake_pen.html",            title: "Retake Your Pen", subtitle: "How to be resilient and hear almost anything", part: 2 },
            { num: 11, file: "chapter_11_move_action.html",           title: "Move to Action", subtitle: "How to turn crucial conversations into action and results", part: 3 },
            { num: 12, file: "chapter_12_yeah_but.html",              title: "Yeah, But", subtitle: "Advice for tough cases", part: 3 },
            { num: 13, file: "chapter_13_putting_together.html",      title: "Putting It All Together", subtitle: "Tools for preparing and learning", part: 3 },
        ];

        const PART_LABELS = {
            1: "Part I \\u2014 Before You Open Your Mouth",
            2: "Part II \\u2014 How to Open Your Mouth",
            3: "Part III \\u2014 How to Finish"
        };

'''

DIGEST_STUBS = """
        // Digest stub functions (no digest modals in this chapter)
        function openDigest(n) {}
        function closeDigest(n) {}
        function closeAllDigests() {}
"""

DROPDOWN_AND_CROSSCHAPTER_JS = """
        // ============================================================
        // CHAPTER DROPDOWN
        // ============================================================
        function buildDropdown() {
            const menu = document.getElementById('dropdownMenu');
            menu.innerHTML = '';
            let currentPart = 0;

            CHAPTERS.forEach((ch, idx) => {
                if (ch.part !== currentPart) {
                    currentPart = ch.part;
                    if (idx > 0) {
                        const divider = document.createElement('div');
                        divider.className = 'dropdown-divider';
                        menu.appendChild(divider);
                    }
                    const label = document.createElement('div');
                    label.className = 'dropdown-section-label';
                    label.textContent = PART_LABELS[currentPart];
                    menu.appendChild(label);
                }

                const item = document.createElement('div');
                item.className = 'chapter-dropdown-item' + (idx === CURRENT_CHAPTER_INDEX ? ' active' : '');
                item.setAttribute('role', 'menuitem');
                item.setAttribute('tabindex', '0');
                item.innerHTML = `
                    <span class="ch-num">${ch.num}</span>
                    <span class="ch-info">
                        <span class="ch-title">${ch.title}</span>
                        <span class="ch-subtitle">${ch.subtitle}</span>
                    </span>
                `;
                item.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    closeDropdown();
                    if (idx !== CURRENT_CHAPTER_INDEX) {
                        window.location.href = ch.file;
                    }
                });
                item.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        closeDropdown();
                        if (idx !== CURRENT_CHAPTER_INDEX) {
                            window.location.href = ch.file;
                        }
                    }
                });
                menu.appendChild(item);
            });

            const divider = document.createElement('div');
            divider.className = 'dropdown-divider';
            menu.appendChild(divider);
            const backItem = document.createElement('div');
            backItem.className = 'chapter-dropdown-item';
            backItem.setAttribute('role', 'menuitem');
            backItem.setAttribute('tabindex', '0');
            backItem.innerHTML = `
                <span class="ch-num" style="background:#333;color:white;border-color:#333;">\\u2630</span>
                <span class="ch-info"><span class="ch-title">Back to Chapter Select</span></span>
            `;
            backItem.addEventListener('click', (e) => { e.preventDefault(); e.stopPropagation(); window.location.href = '../index.html'; });
            backItem.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); window.location.href = '../index.html'; } });
            menu.appendChild(backItem);
        }

        const dropdownBtn = document.getElementById('dropdownBtn');
        const dropdownMenu = document.getElementById('dropdownMenu');

        function toggleDropdown() {
            const isOpen = dropdownMenu.classList.contains('open');
            if (isOpen) closeDropdown(); else openDropdown();
        }

        function openDropdown() {
            dropdownMenu.classList.add('open');
            dropdownBtn.classList.add('open');
            dropdownBtn.setAttribute('aria-expanded', 'true');
        }

        function closeDropdown() {
            dropdownMenu.classList.remove('open');
            dropdownBtn.classList.remove('open');
            dropdownBtn.setAttribute('aria-expanded', 'false');
        }

        dropdownBtn.addEventListener('click', toggleDropdown);

        document.addEventListener('click', (e) => {
            if (!e.target.closest('.chapter-dropdown-wrapper')) closeDropdown();
        });

        // ============================================================
        // CROSS-CHAPTER NAVIGATION
        // ============================================================
        function goToNextChapter() {
            if (CURRENT_CHAPTER_INDEX < CHAPTERS.length - 1) {
                window.location.href = CHAPTERS[CURRENT_CHAPTER_INDEX + 1].file;
            }
        }

        function goToPrevChapter() {
            if (CURRENT_CHAPTER_INDEX > 0) {
                window.location.href = CHAPTERS[CURRENT_CHAPTER_INDEX - 1].file + '?slide=last';
            } else {
                window.location.href = '../index.html';
            }
        }

        function updateChapterNavButtons() {
            const prevBtn = document.getElementById('prevChapterBtn');
            const nextBtn = document.getElementById('nextChapterBtn');
            if (prevBtn) prevBtn.disabled = CURRENT_CHAPTER_INDEX === 0;
            if (nextBtn) nextBtn.disabled = CURRENT_CHAPTER_INDEX === CHAPTERS.length - 1;
        }
"""

NEW_NEXT_PREV = """        function nextSlide() {
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
        }"""

NEW_KEYBOARD_AND_INIT = """        document.addEventListener('keydown', function(event) {
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
                const digestBtn = activeSlide?.querySelector('.digest-pill[data-digest]');
                const digestId = digestBtn?.getAttribute('data-digest');
                if (digestId) { openDigest(Number(digestId)); }
            } else if (event.key === 'a' || event.key === 'A') {
                toggleAutoAdvance();
            } else if (event.key === 'd' || event.key === 'D') {
                if (anyDigestOpen) { closeAllDigests(); return; }
                const activeSlide = document.querySelector('.slide.active');
                const digestBtn = activeSlide?.querySelector('.digest-pill[data-digest]');
                const digestId = digestBtn?.getAttribute('data-digest');
                if (digestId) { openDigest(Number(digestId)); }
            }
        });

        // ============================================================
        // DEEP LINKING
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
        updateChapterNavButtons();
        if (!handleURLParams()) { showSlide(0); }
    </script>"""


# ============================================================
# PROCESSING
# ============================================================

def process_chapter(idx):
    ch = CHAPTERS[idx]
    filepath = os.path.join(SLIDEDECKS_DIR, ch["file"])

    if not os.path.exists(filepath):
        print(f"  FILE NOT FOUND: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []
    warnings = []

    # --- CSS ---

    # 1. Persistent header CSS
    if OLD_PERSISTENT_CSS in content:
        content = content.replace(OLD_PERSISTENT_CSS, NEW_PERSISTENT_CSS, 1)
        changes.append("persistent-header CSS")
    else:
        warnings.append("persistent-header CSS not found")

    # 2. Header CSS
    if OLD_HEADER_CSS in content:
        content = content.replace(OLD_HEADER_CSS, NEW_HEADER_CSS, 1)
        changes.append("header CSS")
    else:
        warnings.append("header CSS not found")

    # 3. Remove .slide-counter CSS if present
    old_sc = "        .slide-counter {\n            position: fixed;\n            top: 15px;\n            right: 30px;\n            background: #333;\n            color: white;\n            padding: 8px 15px;\n            border-radius: 5px;\n            font-size: 14px;\n            z-index: 1001;\n        }\n\n        .auto-advance-toggle {"
    if old_sc in content:
        content = content.replace(old_sc, "        .auto-advance-toggle {", 1)
        changes.append("removed slide-counter CSS")

    # 4. Chapter nav CSS before </style>
    if ".nav-btn.chapter-nav-btn" not in content:
        content = content.replace("    </style>", CHAPTER_NAV_CSS + "\n    </style>", 1)
        changes.append("chapter-nav CSS")

    # 5. Prefetch links
    if 'rel="prefetch"' not in content:
        prefetch = get_prefetch_links(idx)
        content = content.replace("</head>", prefetch + "\n</head>", 1)
        changes.append("prefetch links")

    # --- HTML ---

    # 6. Header HTML (single-line version)
    old_hdr = '    <header class="header" role="banner">CrucialLearning.com | 800.449.5989</header>'
    if old_hdr in content:
        content = content.replace(old_hdr, NEW_HEADER_HTML, 1)
        changes.append("header HTML")

    # 7. Persistent header HTML (regex for varying titles)
    ph_pat = r'    <div class="persistent-header" id="persistentHeader">\s*<h2>.*?</h2>\s*</div>'
    new_ph = get_persistent_header_html(ch)
    if re.search(ph_pat, content, re.DOTALL):
        content = re.sub(ph_pat, new_ph, content, count=1, flags=re.DOTALL)
        changes.append("persistent-header HTML")
    else:
        warnings.append("persistent-header HTML not found")

    # 8. Nav bar - add prev chapter button
    old_nav_start = '        <button class="nav-btn" onclick="previousSlide()" aria-label="Previous slide">\u2190 Previous</button>'
    new_nav_start = '        <button class="nav-btn chapter-nav-btn" id="prevChapterBtn" onclick="goToPrevChapter()" aria-label="Previous chapter">\u25c4 Prev Ch.</button>\n        <button class="nav-btn" onclick="previousSlide()" aria-label="Previous slide">\u2190 Back</button>'
    if old_nav_start in content:
        content = content.replace(old_nav_start, new_nav_start, 1)
        changes.append("prev chapter btn")

    # 9. Nav bar - add next chapter button
    old_nav_end = '        <button class="nav-btn" onclick="nextSlide()" aria-label="Next slide">Next \u2192</button>\n    </nav>'
    new_nav_end = '        <button class="nav-btn" onclick="nextSlide()" aria-label="Next slide">Next \u2192</button>\n        <button class="nav-btn chapter-nav-btn" id="nextChapterBtn" onclick="goToNextChapter()" aria-label="Next chapter">Next Ch. \u25ba</button>\n    </nav>'
    if old_nav_end in content:
        content = content.replace(old_nav_end, new_nav_end, 1)
        changes.append("next chapter btn")

    # --- JS ---

    # 10. CHAPTERS data
    if 'CURRENT_CHAPTER_INDEX' not in content:
        ch_js = CHAPTERS_JS_BLOCK + f"        const CURRENT_CHAPTER_INDEX = {idx}; // Chapter {idx + 1}\n\n"
        content = content.replace(
            "    <script>\n        let currentSlide = 0;",
            "    <script>\n" + ch_js + "        let currentSlide = 0;",
            1
        )
        changes.append("CHAPTERS data")

    # 11. Digest stubs (if no digest functions exist)
    if 'function closeAllDigests' not in content:
        content = content.replace(
            "        function getSlideDuration() {",
            DIGEST_STUBS + "\n        function getSlideDuration() {",
            1
        )
        changes.append("digest stubs")

    # 12. Dropdown + cross-chapter functions (before showSlide)
    if 'function buildDropdown' not in content:
        content = content.replace(
            "        function showSlide(n) {",
            DROPDOWN_AND_CROSSCHAPTER_JS + "\n        function showSlide(n) {",
            1
        )
        changes.append("dropdown + cross-chapter JS")

    # 13. Fix showSlide modular arithmetic
    old_mod = "            currentSlide = (n + totalSlides) % totalSlides;"
    new_clamp = "            currentSlide = Math.max(0, Math.min(n, totalSlides - 1));"
    if old_mod in content:
        content = content.replace(old_mod, new_clamp, 1)
        changes.append("showSlide clamping")

    # 14. Replace nextSlide/previousSlide
    old_np = "        function nextSlide() {\n            showSlide(currentSlide + 1);\n        }\n\n        function previousSlide() {\n            showSlide(currentSlide - 1);\n        }"
    if old_np in content:
        content = content.replace(old_np, NEW_NEXT_PREV, 1)
        changes.append("boundary nextSlide/previousSlide")

    # 15. Replace keyboard handler + init (regex: keydown listener through showSlide(0);</script>)
    kb_pat = r"        document\.addEventListener\('keydown'.*?\}\);\s*\n\s*showSlide\(0\);\s*\n\s*</script>"
    if re.search(kb_pat, content, re.DOTALL):
        content = re.sub(kb_pat, NEW_KEYBOARD_AND_INIT, content, count=1, flags=re.DOTALL)
        changes.append("keyboard handler + deep linking + init")
    else:
        warnings.append("keyboard handler pattern not found")

    # --- WRITE ---
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  \u2713 Applied {len(changes)} changes: {', '.join(changes)}")
        if warnings:
            for w in warnings:
                print(f"  \u26a0 {w}")
        return True
    else:
        print(f"  No changes applied")
        if warnings:
            for w in warnings:
                print(f"  \u26a0 {w}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Propagating chapter navigation to slidedecks...")
    print("=" * 60)

    updated = 0
    for idx in range(1, 13):  # Chapters 2-13 (index 1-12)
        ch = CHAPTERS[idx]
        print(f"\nCh {ch['num']}: {ch['title']}")
        if process_chapter(idx):
            updated += 1

    print(f"\n{'=' * 60}")
    print(f"Done! Updated {updated} of 12 chapter files.")
    print(f"Chapter 1 was already the reference implementation.")
    print(f"\nNext: spot-check a few chapters in the browser.")
