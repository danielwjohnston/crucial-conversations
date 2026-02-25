#!/usr/bin/env python3
"""Rebuild chapters 8-13 to match best practices."""

import pathlib

ROOT = pathlib.Path('/Users/dwjohnston/Library/CloudStorage/OneDrive-TEGNA/Desktop/Crucial Conversations/slidedecks')

# Read Ch6 JS as template
ch6 = (ROOT / 'chapter_06_learn_to_look.html').read_text()
JS_START = ch6.find('<script>') + 8
JS_END = ch6.find('</script>')
BASE_JS = ch6[JS_START:JS_END]

def make_js(chapter_index, durations_str):
    js = BASE_JS.replace(
        'const CURRENT_CHAPTER_INDEX = 5;',
        f'const CURRENT_CHAPTER_INDEX = {chapter_index};'
    )
    old_start = js.find('// 14 slides')
    old_end = js.find('];', js.find('DURATIONS_SECONDS')) + 2
    old_dur = js[old_start:old_end]
    js = js.replace(old_dur, durations_str)
    return js

NAV_HTML = """    <nav class="navigation" role="navigation" aria-label="Slide navigation">
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
    </nav>"""

def build(filename, title_short, ch_num, subtitle, prev_file, next_file, 
          header_title, header_subtitle, slides, modals, chapter_index, durations):
    head_links = ""
    if prev_file:
        head_links += f'    <link rel="prefetch" href="{prev_file}">\n'
    if next_file:
        head_links += f'    <link rel="prefetch" href="{next_file}">'
    
    js = make_js(chapter_index, durations)
    
    slides_html = "\n\n".join(f"        {s}" for s in slides)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Leadership Bookclub - {title_short}</title>
    <link rel="stylesheet" href="shared.css">
{head_links}
</head>
<body>
    <a class="skip-link" href="#main-content">Skip to content</a>

    <header class="header" role="banner">
        <span class="header-brand">CrucialLearning.com | 800.449.5989</span>
        <span class="header-slide-counter" id="slideCounter">
            <span id="slideNumber">1</span> / <span id="totalSlides">0</span>
        </span>
    </header>

    <footer class="footer" role="contentinfo">
        &copy;2026 Leadership Development. All rights reserved.
    </footer>

    <main id="main-content" class="slideshow-container" aria-label="Slideshow presentation">
        <div id="timerAria" class="sr-only" aria-live="polite" aria-atomic="true"></div>

        <div class="persistent-header" id="chapterHeader">
            <div class="persistent-header-left">
                <span class="persistent-header-title" id="headerTitle">{header_title}</span>
                <span class="persistent-header-subtitle" id="headerSubtitle">{header_subtitle}</span>
            </div>
            <div class="chapter-dropdown-wrapper">
                <button class="chapter-dropdown-btn" id="dropdownBtn" aria-expanded="false" aria-haspopup="true">
                    Chapters <span class="arrow">&#9660;</span>
                </button>
                <div class="chapter-dropdown-menu" id="dropdownMenu" role="menu">
                </div>
            </div>
        </div>

{slides_html}

    </main>

    <!-- Digest Modals -->
{modals}

{NAV_HTML}

    <script>{js}</script>
</body>
</html>"""
    
    path = ROOT / filename
    path.write_text(html)
    print(f"  {filename}: {len(html):,} chars, {len(slides)} slides")
    return html


# ============================================================
# CHAPTER 8: STATE My Path
# ============================================================
def build_ch8():
    slides = [
        # 1: Title
        """<!-- Slide 1: Title -->
        <div class="slide active title-slide">
            <div class="slide-content">
                <div class="brand-logo">Leadership Bookclub</div>
                <h1>CHAPTER 8</h1>
                <h2>STATE My Path</h2>
                <p class="subtitle">How to speak persuasively, not abrasively</p>
            </div>
        </div>""",
        
        # 2: Core Message
        """<!-- Slide 2: Core Message -->
        <div class="slide">
            <div class="slide-content">
                <h2>Core Message</h2>
                <div class="highlight">
                    <h3>Be 100% candid AND 100% respectful</h3>
                    <p>The best at dialogue speak their minds <strong>completely</strong> and do it in a way that makes it safe for others to hear and respond.</p>
                </div>
                <h3>Most People Alternate Between:</h3>
                <ul>
                    <li><strong>Bluntly dumping</strong> their ideas</li>
                    <li><strong>Saying nothing</strong> out of fear</li>
                    <li><strong>Sugar-coating</strong> so much the message loses impact</li>
                </ul>
            </div>
        </div>""",
        
        # 3: The STATE Model
        """<!-- Slide 3: The STATE Model -->
        <div class="slide">
            <div class="slide-content">
                <h2>The STATE Model</h2>
                <div class="story-box"><h3><strong>S</strong> &ndash; Share your facts</h3><p>Start with the least controversial, most persuasive elements</p></div>
                <div class="story-box"><h3><strong>T</strong> &ndash; Tell your story</h3><p>Explain what you&#39;re beginning to conclude</p></div>
                <div class="story-box"><h3><strong>A</strong> &ndash; Ask for others&#39; paths</h3><p>Encourage others to share their facts and stories</p></div>
                <div class="story-box"><h3><strong>T</strong> &ndash; Talk tentatively</h3><p>State your story as a story, not as fact</p></div>
                <div class="story-box"><h3><strong>E</strong> &ndash; Encourage testing</h3><p>Make it safe to express differing views</p></div>
            </div>
        </div>""",
        
        # 4: Share Facts + Tell Story
        """<!-- Slide 4: Share Facts + Tell Story -->
        <div class="slide">
            <div class="slide-content">
                <h2>Share Facts &amp; Tell Your Story</h2>
                <div class="two-column">
                    <div class="column-box">
                        <h4>Share Your Facts</h4>
                        <p>Facts are <strong>least controversial</strong> and most persuasive. They lay the groundwork for your conclusion.</p>
                        <p style="margin-top:10px;"><em>&ldquo;You arrived at 8:20 AM&rdquo;</em> (fact) vs <em>&ldquo;You can&#39;t be trusted&rdquo;</em> (judgment)</p>
                    </div>
                    <div class="column-box">
                        <h4>Tell Your Story</h4>
                        <p>After sharing facts, explain your conclusion <strong>tentatively</strong>&mdash;as a possible story, not proven fact.</p>
                        <p style="margin-top:10px;"><em>&ldquo;I&#39;m beginning to wonder if you don&#39;t trust me. Is that what&#39;s going on?&rdquo;</em></p>
                    </div>
                </div>
            </div>
        </div>""",
        
        # 5: Ask, Talk Tentatively, Encourage Testing
        """<!-- Slide 5: Ask, Talk Tentatively, Encourage Testing -->
        <div class="slide">
            <div class="slide-content">
                <h2>Ask, Talk Tentatively, Encourage Testing</h2>
                <div class="story-box">
                    <h3>Ask for Others&#39; Paths</h3>
                    <p>&ldquo;How do you see it?&rdquo; &bull; &ldquo;What&#39;s your perspective?&rdquo; &bull; Be willing to reshape your story.</p>
                </div>
                <div class="story-box">
                    <h3>Talk Tentatively (Not Wimpy)</h3>
                    <p>&ldquo;I&#39;m beginning to conclude...&rdquo; shares opinion. &ldquo;I know this is probably not true...&rdquo; is wimpy.</p>
                </div>
                <div class="story-box">
                    <h3>Encourage Testing</h3>
                    <p>The limit of how strongly you express your opinion = your willingness to have it challenged.</p>
                    <p><em>&ldquo;Does anyone see it differently?&rdquo;</em></p>
                </div>
            </div>
        </div>""",
        
        # 6: Discussion Break #1
        """<!-- Slide 6: Discussion Break #1 -->
        <div class="slide discussion-slide">
            <div class="slide-content">
                <h2>Discussion Break #1</h2>
                <div class="discussion-question">
                    <p>Think of a recent conversation where you jumped straight to your conclusion instead of starting with facts. How might walking through the STATE steps&mdash;facts first, then story, then asking&mdash;have changed the outcome?</p>
                </div>
                <button class="digest-pill" type="button" data-digest="1" onclick="openDigest(1)" aria-haspopup="dialog" aria-controls="digestModal1">
                    <span class="dot" aria-hidden="true"></span>
                    Dan&#39;s Digest
                </button>
            </div>
        </div>""",
        
        # 7: The Goldilocks Test
        """<!-- Slide 7: The Goldilocks Test -->
        <div class="slide">
            <div class="slide-content">
                <h2>The Goldilocks Test</h2>
                <h3>Not too soft, not too harsh&mdash;just right</h3>
                <div class="three-column">
                    <div class="column-box" style="border-color:#4a90e2;">
                        <h4 style="color:#4a90e2;">Understated</h4>
                        <p><em>&ldquo;This is probably stupid, but...&rdquo;</em></p>
                        <p><em>&ldquo;I&#39;m ashamed to mention this...&rdquo;</em></p>
                    </div>
                    <div class="column-box" style="border-color:#e30613;">
                        <h4>Overstated</h4>
                        <p><em>&ldquo;How come you ripped us off?&rdquo;</em></p>
                        <p><em>&ldquo;When did you start using drugs?&rdquo;</em></p>
                    </div>
                    <div class="column-box" style="border-color:#48bb78;">
                        <h4 style="color:#38a169;">Just Right</h4>
                        <p><em>&ldquo;It appears you&#39;re taking this home. Is that right?&rdquo;</em></p>
                        <p><em>&ldquo;This is leading me to conclude... Do you have another explanation?&rdquo;</em></p>
                    </div>
                </div>
            </div>
        </div>""",
        
        # 8: STATE in Action
        """<!-- Slide 8: STATE in Action - The Missing Money -->
        <div class="slide">
            <div class="slide-content">
                <h2>STATE in Action: The Missing Money</h2>
                <div class="story-box">
                    <h3>S &ndash; Share Facts</h3>
                    <p><em>&ldquo;I was planning to use $40 from my wallet. The money wasn&#39;t there. I remembered you asking for money last night. I told you no, and you went out anyway.&rdquo;</em></p>
                    <h3 style="margin-top:15px;">T &ndash; Tell Story</h3>
                    <p><em>&ldquo;Obviously, one possibility is that you took the money.&rdquo;</em></p>
                    <h3 style="margin-top:15px;">A &ndash; Ask</h3>
                    <p><em>&ldquo;I hope you can see how I might have the question. Did you?&rdquo;</em></p>
                </div>
                <div class="highlight">
                    <strong>Result:</strong> Amber admitted she took it, planning to put it back. They talked honestly. There were consequences&mdash;but also connection.
                </div>
            </div>
        </div>""",
        
        # 9: The Irony of Dialogue
        """<!-- Slide 9: The Irony of Dialogue -->
        <div class="slide">
            <div class="slide-content">
                <h2>The Irony of Dialogue</h2>
                <div class="bridge-box">
                    <h3>A Counterintuitive Truth</h3>
                    <p style="margin-top: 20px; font-size: 1.2em;"><strong>The more convinced and forceful you act, the more resistant others become.</strong></p>
                    <p style="margin-top: 20px;">Speaking in absolute terms doesn&#39;t increase your influence&mdash;it <strong>decreases</strong> it.</p>
                    <p style="margin-top: 20px;">The converse: <strong>the more tentatively you speak, the more open people become</strong> to your opinions.</p>
                </div>
            </div>
        </div>""",
        
        # 10: Discussion Break #2
        """<!-- Slide 10: Discussion Break #2 -->
        <div class="slide discussion-slide">
            <div class="slide-content">
                <h2>Discussion Break #2</h2>
                <div class="discussion-question">
                    <p>Which step of STATE feels most challenging for you&mdash;and why? Have you experienced the &ldquo;irony of dialogue&rdquo; where pushing harder actually made someone more resistant?</p>
                </div>
                <button class="digest-pill" type="button" data-digest="2" onclick="openDigest(2)" aria-haspopup="dialog" aria-controls="digestModal2">
                    <span class="dot" aria-hidden="true"></span>
                    Dan&#39;s Digest
                </button>
            </div>
        </div>""",
        
        # 11: This Week's Challenge
        """<!-- Slide 11: This Week's Challenge -->
        <div class="slide">
            <div class="slide-content">
                <h2>This Week&#39;s Challenge</h2>
                <div class="highlight">
                    <h3>Practice STATE in one conversation:</h3>
                    <ul>
                        <li><strong>Prepare your facts</strong> before the conversation</li>
                        <li><strong>Tell your story tentatively</strong>&mdash;not as absolute truth</li>
                        <li><strong>Ask for their perspective</strong> and genuinely listen</li>
                        <li><strong>Encourage testing</strong>&mdash;make it safe to disagree</li>
                    </ul>
                </div>
                <p style="margin-top: 18px;"><strong>Next Meeting:</strong> Share how using STATE changed a conversation</p>
            </div>
        </div>""",
        
        # 12: More to Ponder
        """<!-- Slide 12: More to Ponder -->
        <div class="slide">
            <div class="slide-content">
                <h2>More to Ponder</h2>
                <p class="subtitle">Use these as a quick review of key takeaways and ideas to keep thinking about.</p>
                <div class="story-box">
                    <h3>Choose 1&ndash;2 prompts</h3>
                    <ul>
                        <li>Why does starting with facts make your conclusion more persuasive&mdash;and less offensive?</li>
                        <li>What&#39;s the difference between being tentative and being wimpy?</li>
                        <li>How do confidence and humility work together in STATE?</li>
                        <li>When you&#39;re sure you&#39;re right, what happens to your influence&mdash;and why?</li>
                    </ul>
                </div>
            </div>
        </div>""",
        
        # 13: Look Ahead
        """<!-- Slide 13: Look Ahead -->
        <div class="slide look-ahead-slide">
            <div class="slide-content">
                <h1>Look Ahead</h1>
                <h2>Chapter 9: Explore Others&#39; Paths</h2>
                <div class="highlight" style="margin-top: 10px;">
                    <h3>What we&#39;ll focus on next</h3>
                    <ul>
                        <li><strong>How to listen</strong> when others blow up or clam up</li>
                        <li>The <strong>AMPP</strong> framework: Ask, Mirror, Paraphrase, Prime</li>
                        <li>Helping others <strong>retrace their Path to Action</strong></li>
                    </ul>
                </div>
                <p class="subtitle" style="margin-top: 18px;"><strong>Optional prep:</strong> Notice a conversation this week where someone shut down or exploded. What happened?</p>
            </div>
        </div>""",
    ]
    
    modals = """    <div class="digest-modal" id="digestModal1" role="dialog" aria-labelledby="digestTitle1" aria-modal="true">
        <div class="digest-content">
            <button class="digest-close" onclick="closeDigest(1)" aria-label="Close">&times;</button>
            <h2 id="digestTitle1">Dan&#39;s Digest</h2>
            <div class="digest-answer">
                <h4>Answer Key (Discussion Break #1)</h4>
                <p><strong>Facts first:</strong> When we&#39;re emotional, we start with stories and conclusions&mdash;the most controversial way to begin. Facts are least controversial and most persuasive because they&#39;re observable and verifiable.</p>
                <p style="margin-top: 12px;"><strong>The Path to Action:</strong> See/Hear &rarr; Story &rarr; Feel &rarr; Act. When sharing, retrace this path: start with what you saw, then what you concluded, then how you feel. This helps others follow your reasoning.</p>
                <p style="margin-top: 12px;"><strong>Tentative ≠ Wimpy:</strong> &ldquo;I&#39;m beginning to conclude...&rdquo; is tentative (shares opinion). &ldquo;I know this is probably not true...&rdquo; is wimpy (undermines your credibility).</p>
            </div>
            <div class="digest-insights">
                <h4>Key Points</h4>
                <ul>
                    <li>Facts prevent others from telling villain stories about you</li>
                    <li>Your opinions deserve to be in the pool&mdash;but so do others&#39;</li>
                    <li>Confidence + Humility + Skill = effective candor</li>
                </ul>
            </div>
        </div>
    </div>

    <div class="digest-modal" id="digestModal2" role="dialog" aria-labelledby="digestTitle2" aria-modal="true">
        <div class="digest-content">
            <button class="digest-close" onclick="closeDigest(2)" aria-label="Close">&times;</button>
            <h2 id="digestTitle2">Dan&#39;s Digest</h2>
            <div class="digest-answer">
                <h4>Answer Key (Discussion Break #2)</h4>
                <p><strong>The irony:</strong> The more forcefully you push your view, the more resistance you create. Speaking in absolutes decreases influence; speaking tentatively increases it.</p>
                <p style="margin-top: 12px;"><strong>Encourage testing:</strong> The only limit to how strongly you can express your opinion is your willingness to be equally vigorous in encouraging others to challenge it.</p>
                <p style="margin-top: 12px;"><strong>When you&#39;re dying to win:</strong> Check yourself&mdash;is your goal to WIN or to LEARN? The harder STATE feels, the more likely you&#39;re trying to win.</p>
            </div>
            <div class="digest-insights">
                <h4>Key Points</h4>
                <ul>
                    <li>The Goldilocks test: not too soft, not too harsh&mdash;just right</li>
                    <li>When you start with shocking conclusions, people assume you&#39;re either stupid or evil</li>
                    <li>Back off and ask: What do I really want?</li>
                </ul>
            </div>
        </div>
    </div>"""
    
    durations = """// 13 slides
        const DURATIONS_SECONDS = [
            30,   // 1  Title
            90,   // 2  Core Message
            120,  // 3  STATE Model
            150,  // 4  Share Facts + Tell Story
            150,  // 5  Ask + Talk Tentatively + Encourage
            300,  // 6  Discussion Break #1
            120,  // 7  Goldilocks Test
            150,  // 8  STATE in Action
            90,   // 9  Irony of Dialogue
            300,  // 10 Discussion Break #2
            90,   // 11 This Week's Challenge
            120,  // 12 More to Ponder
            60,   // 13 Look Ahead
        ];"""
    
    build("chapter_08_state_path.html", "STATE My Path", 8, 
          "How to speak persuasively, not abrasively",
          "chapter_07_make_safe.html", "chapter_09_explore_paths.html",
          "Ch. 8: STATE MY PATH", "How to speak persuasively, not abrasively",
          slides, modals, 7, durations)

# Run
print("Building Ch8...")
build_ch8()
print("Done!")
