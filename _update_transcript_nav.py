#!/usr/bin/env python3
"""Update nav-footer in all transcript pages to use arrow-button style navigation."""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
TRANSCRIPT_DIR = os.path.join(ROOT, "resources", "transcripts")
AUDIO_DIR = os.path.join(TRANSCRIPT_DIR, "audio")

# New CSS to replace the plain-link nav-footer with arrow buttons
NEW_NAV_CSS = """        .nav-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 48px;
            padding-top: 20px;
            border-top: 2px solid var(--border-color);
            font-size: 0.95rem;
            gap: 12px;
        }
        .nav-footer a {
            color: var(--blue);
            text-decoration: none;
            font-weight: 600;
        }
        .nav-footer a:hover { text-decoration: underline; }
        .nav-btn {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 10px 18px;
            background: var(--brand-red);
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.9rem;
            text-decoration: none;
            cursor: pointer;
            transition: background 0.2s, transform 0.15s;
            white-space: nowrap;
        }
        .nav-btn:hover { background: var(--brand-red-accessible); transform: translateY(-1px); color: white; text-decoration: none; }
        .nav-btn.secondary { background: #555; }
        .nav-btn.secondary:hover { background: #333; }
        .nav-btn.disabled { opacity: 0.35; pointer-events: none; }
        .nav-center { text-align: center; }"""

OLD_NAV_CSS_PAT = re.compile(
    r'        \.nav-footer \{.*?\}.*?'
    r'\.nav-footer a \{.*?\}.*?'
    r'\.nav-footer a:hover \{[^}]*\}',
    re.DOTALL
)

def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Replace nav CSS block
    if '.nav-btn' not in html:
        m = OLD_NAV_CSS_PAT.search(html)
        if m:
            html = html[:m.start()] + NEW_NAV_CSS + html[m.end():]

    # 2. Replace <nav class="nav-footer"> block with arrow-button version
    nav_pat = re.compile(r'<nav class="nav-footer">\s*(.*?)\s*</nav>', re.DOTALL)
    m = nav_pat.search(html)
    if not m:
        return False

    inner = m.group(1)
    # Parse existing links
    link_pat = re.compile(r'<a href="([^"]+)">(.*?)</a>')
    links = link_pat.findall(inner)
    # Also check for <span></span> placeholder (means no prev)
    has_empty_span = '<span></span>' in inner or '<span>' in inner

    prev_href = prev_label = next_href = next_label = index_href = None
    for href, label in links:
        clean = re.sub(r'&[a-z]+;', '', label).strip()
        if 'index.html' in href or 'All Transcript' in clean:
            index_href = href
        elif clean.endswith('→') or clean.endswith('>') or '→' in label or '&rarr;' in label:
            next_href = href
            next_label = re.sub(r'\s*&rarr;', '', label).strip()
            next_label = re.sub(r'\s*→', '', next_label).strip()
        else:
            prev_href = href
            prev_label = re.sub(r'&larr;\s*', '', label).strip()
            prev_label = re.sub(r'←\s*', '', prev_label).strip()

    if not index_href:
        index_href = '../index.html' if '/audio/' in path else 'index.html'

    # Build new nav
    parts = []
    if prev_href and prev_label:
        parts.append(f'        <a href="{prev_href}" class="nav-btn">&#x25C0; {prev_label}</a>')
    else:
        parts.append('        <span class="nav-btn disabled">&#x25C0; Prev</span>')

    parts.append(f'        <a href="{index_href}" class="nav-btn secondary">All Transcripts</a>')

    if next_href and next_label:
        parts.append(f'        <a href="{next_href}" class="nav-btn">{next_label} &#x25B6;</a>')
    else:
        parts.append('        <span class="nav-btn disabled">Next &#x25B6;</span>')

    new_nav = '    <nav class="nav-footer">\n' + '\n'.join(parts) + '\n    </nav>'
    html = html[:m.start()] + new_nav + html[m.end():]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return True

# Process all transcript files
count = 0
for pat in [os.path.join(TRANSCRIPT_DIR, 'chapter_*.html'),
            os.path.join(AUDIO_DIR, 'audio_*.html')]:
    for path in sorted(glob.glob(pat)):
        if update_file(path):
            count += 1
            print(f"  ✓ {os.path.basename(path)}")
        else:
            print(f"  ✗ {os.path.basename(path)} (no nav found)")

print(f"\nUpdated {count} files")
