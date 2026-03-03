#!/usr/bin/env python3
"""Inject HTML5 audio players into audiobook transcript pages."""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(ROOT, "resources", "transcripts", "audio")
MEDIA_REL = "../../media/audio"  # relative path from transcript/audio/ to media/audio/

# Mapping: transcript filename -> M4A filename (with spaces)
FILE_MAP = {
    "audio_opening.html":   "01 Opening Credits.m4a",
    "audio_publisher.html": "02 Publisher's Note.m4a",
    "audio_preface.html":   "03 Preface.m4a",
    "audio_01.html":        "04 1 What\u2019s a Crucial Conversation.m4a",
    "audio_02.html":        "05 2 Mastering Crucial Conversations.m4a",
    "audio_part1.html":     "06 Part I- What to Do Before You Open Your Mouth.m4a",
    "audio_03.html":        "07 3 Choose Your Topic.m4a",
    "audio_04.html":        "08 4 Start with Heart.m4a",
    "audio_05.html":        "09 5 Master My Stories.m4a",
    "audio_part2.html":     "10 Part II- How to Open Your Mouth.m4a",
    "audio_06.html":        "11 6 Learn to Look.m4a",
    "audio_07.html":        "12 7 Make It Safe.m4a",
    "audio_08.html":        "13 8 STATE My Path.m4a",
    "audio_09.html":        "14 9 Explore Others\u2019 Paths.m4a",
    "audio_10.html":        "15 10 Retake Your Pen.m4a",
    "audio_part3.html":     "16 Part III- How to Finish.m4a",
    "audio_11.html":        "17 11 Move to Action.m4a",
    "audio_12.html":        "18 12 Yeah, But.m4a",
    "audio_13.html":        "19 13 Putting It All Together.m4a",
    "audio_closing.html":   "20 End Credits.m4a",
}

# CSS for the audio player widget
PLAYER_CSS = """
        /* === Audio Player === */
        .audio-player {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 12px;
            padding: 20px 24px;
            margin: 0 0 32px;
            display: flex;
            align-items: center;
            gap: 16px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }
        .audio-player .play-icon {
            width: 48px;
            height: 48px;
            background: var(--brand-red);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            cursor: pointer;
            transition: background 0.2s, transform 0.15s;
        }
        .audio-player .play-icon:hover {
            background: var(--brand-red-accessible);
            transform: scale(1.08);
        }
        .audio-player .play-icon svg {
            width: 20px;
            height: 20px;
            fill: white;
            margin-left: 2px;
        }
        .audio-player .player-body { flex: 1; min-width: 0; }
        .audio-player .player-label {
            color: rgba(255,255,255,0.6);
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 700;
            margin-bottom: 6px;
        }
        .audio-player audio {
            width: 100%;
            height: 36px;
            border-radius: 6px;
        }
        .audio-player audio::-webkit-media-controls-panel {
            background: rgba(255,255,255,0.08);
        }
        .audio-player .speed-controls {
            display: flex;
            gap: 4px;
            margin-top: 8px;
        }
        .audio-player .speed-btn {
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.15);
            color: rgba(255,255,255,0.7);
            font-size: 0.7rem;
            padding: 3px 8px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.15s;
        }
        .audio-player .speed-btn:hover,
        .audio-player .speed-btn.active {
            background: var(--brand-red);
            border-color: var(--brand-red);
            color: white;
        }
        @media print {
            .audio-player { display: none; }
        }
        @media (max-width: 600px) {
            .audio-player { flex-direction: column; text-align: center; padding: 16px; }
            .audio-player .play-icon { display: none; }
        }"""

def url_encode_filename(name):
    """Percent-encode the filename for use in HTML src attribute."""
    return name.replace(' ', '%20').replace("'", '%27').replace('\u2019', '%E2%80%99').replace('-', '-')

def get_player_html(m4a_filename):
    """Generate the audio player HTML block."""
    src = f"{MEDIA_REL}/{url_encode_filename(m4a_filename)}"
    return f"""    <div class="audio-player">
        <div class="play-icon" onclick="var a=this.closest('.audio-player').querySelector('audio');if(a.paused)a.play();else a.pause();" title="Play / Pause">
            <svg viewBox="0 0 24 24"><polygon points="6,3 20,12 6,21"/></svg>
        </div>
        <div class="player-body">
            <div class="player-label">Listen to this chapter</div>
            <audio controls preload="metadata">
                <source src="{src}" type="audio/mp4">
                Your browser does not support the audio element.
            </audio>
            <div class="speed-controls">
                <button class="speed-btn" onclick="setSpeed(this,0.75)">0.75x</button>
                <button class="speed-btn active" onclick="setSpeed(this,1)">1x</button>
                <button class="speed-btn" onclick="setSpeed(this,1.25)">1.25x</button>
                <button class="speed-btn" onclick="setSpeed(this,1.5)">1.5x</button>
                <button class="speed-btn" onclick="setSpeed(this,2)">2x</button>
            </div>
        </div>
    </div>
    <script>
    function setSpeed(btn, rate) {{
        const player = btn.closest('.audio-player');
        const audio = player.querySelector('audio');
        audio.playbackRate = rate;
        player.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    }}
    </script>"""

def inject_player(filepath, m4a_filename):
    """Inject audio player CSS and HTML into a transcript page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if already injected
    if 'audio-player' in html:
        return False

    # 1. Inject CSS before the closing </style> — but after existing styles
    css_injection = PLAYER_CSS + "\n"
    # Find the last occurrence of a CSS rule before </style>
    style_close = html.find('    </style>')
    if style_close == -1:
        print(f"  ✗ {os.path.basename(filepath)} — no </style> found")
        return False
    html = html[:style_close] + css_injection + html[style_close:]

    # 2. Inject player HTML right after <article>
    article_tag = '<article>'
    article_pos = html.find(article_tag)
    if article_pos == -1:
        print(f"  ✗ {os.path.basename(filepath)} — no <article> found")
        return False
    insert_pos = article_pos + len(article_tag)
    player_html = "\n" + get_player_html(m4a_filename) + "\n"
    html = html[:insert_pos] + player_html + html[insert_pos:]

    # 3. Update print media query to also hide audio-player
    html = html.replace(
        '.back-link, .nav-footer, .print-btn, .meta { display: none; }',
        '.back-link, .nav-footer, .print-btn, .meta, .audio-player { display: none; }'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return True

# Process all mapped files
count = 0
for transcript_file, m4a_file in FILE_MAP.items():
    filepath = os.path.join(AUDIO_DIR, transcript_file)
    if not os.path.exists(filepath):
        print(f"  ✗ {transcript_file} — file not found")
        continue
    # Verify M4A exists
    m4a_path = os.path.join(ROOT, "resources", "media", "audio", m4a_file)
    if not os.path.exists(m4a_path):
        print(f"  ✗ {transcript_file} — M4A not found: {m4a_file}")
        continue
    if inject_player(filepath, m4a_file):
        count += 1
        print(f"  ✓ {transcript_file} → {m4a_file}")
    else:
        print(f"  · {transcript_file} — already has player or skipped")

print(f"\nInjected audio players into {count} files")
