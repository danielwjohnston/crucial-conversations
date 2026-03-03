#!/usr/bin/env python3
"""Generate per-chapter printable handout pages for resources/handouts/."""
import os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT, "resources", "handouts")

CHAPTERS = [
    {
        "num": 1, "title": "What\u2019s a Crucial Conversation", "subtitle": "And who cares?", "part": 1,
        "key_concepts": [
            ("Crucial Conversation", "A discussion where (1) opinions vary, (2) stakes are high, and (3) emotions run strong."),
            ("Lag Time", "The gap between when a problem emerges and when it\u2019s honestly discussed. Longer lag = more damage."),
            ("Talk It Out or Act It Out", "If you don\u2019t discuss issues, you\u2019ll act them out through sarcasm, withdrawal, or passive aggression."),
            ("Self-Defeating Loops", "Avoiding conversation often creates the very problem you feared."),
        ],
        "discussion": "Think of a recent situation where stakes were high and emotions ran strong. What was the \u2018lag time\u2019 before the issue was addressed? How did that delay affect the relationship or outcome?",
        "reflection": [
            "Identify one crucial conversation you\u2019ve been avoiding.",
            "What stories are you telling yourself about why you haven\u2019t had it?",
            "What would improve if you shortened the lag time?",
        ],
    },
    {
        "num": 2, "title": "Mastering Crucial Conversations", "subtitle": "The power of dialogue", "part": 1,
        "key_concepts": [
            ("Dialogue", "The free flow of meaning between two or more people."),
            ("Pool of Shared Meaning", "Everything that\u2019s been openly shared\u2014ideas, feelings, theories, experiences. A bigger pool leads to better decisions."),
            ("Opinion Leaders", "People admired for their ability to raise risky issues effectively\u2014they shrink lag time."),
            ("Synergy", "When the pool is full, the group can make decisions no single person could have made alone."),
        ],
        "discussion": "When has a group decision been better because everyone contributed honestly to the Pool of Shared Meaning? What happened when meaning was withheld?",
        "reflection": [
            "Rate your comfort level (1\u201310) with speaking up in high-stakes situations.",
            "What\u2019s one thing you could do this week to add more meaning to a shared pool?",
            "Who is an \u2018opinion leader\u2019 you admire? What do they do differently?",
        ],
    },
    {
        "num": 3, "title": "Choose Your Topic", "subtitle": "How to be sure you hold the right conversation", "part": 1,
        "key_concepts": [
            ("CPR Framework", "Content = what happened. Pattern = recurring behavior. Relationship = impact on trust/respect."),
            ("Unbundling", "Separate the multiple issues tangled in a conflict\u2014then choose the one that matters most right now."),
            ("The Right Conversation", "Ask: \u2018What do I really want to resolve?\u2019 Don\u2019t address symptoms when the real issue is deeper."),
            ("Three Signals", "You\u2019re having the wrong conversation if you feel d\u00e9j\u00e0 vu, your emotions escalate beyond the topic, or you\u2019re going in circles."),
        ],
        "discussion": "Think of a recurring frustration at work or home. Is it a Content, Pattern, or Relationship issue? How would naming the right level change the conversation?",
        "reflection": [
            "Write down a current frustration. Is it content, pattern, or relationship?",
            "What\u2019s the \u2018real\u2019 conversation you need to have?",
            "How would you open that conversation in one clear sentence?",
        ],
    },
    {
        "num": 4, "title": "Start with Heart", "subtitle": "How to stay focused on what you really want", "part": 1,
        "key_concepts": [
            ("Start with Heart", "Before opening your mouth, clarify what you really want\u2014for yourself, for the other person, and for the relationship."),
            ("The Fool\u2019s Choice", "The false belief that you must choose between honesty and kindness. Skilled people refuse this trade-off."),
            ("Motive Check", "Ask: \u2018What am I acting like I want?\u2019 vs. \u2018What do I really want?\u2019"),
            ("Refocus", "When emotions spike, pause and return to your original goal."),
        ],
        "discussion": "Describe a time you fell into the Fool\u2019s Choice\u2014choosing silence to keep peace, or aggression to make a point. What would \u2018refusing the Fool\u2019s Choice\u2019 have looked like?",
        "reflection": [
            "What do you really want from an upcoming difficult conversation?",
            "What do you want for the other person?",
            "What do you want for the relationship?",
        ],
    },
    {
        "num": 5, "title": "Master My Stories", "subtitle": "How to stay in dialogue when you\u2019re angry, scared, or hurt", "part": 2,
        "key_concepts": [
            ("Path to Action", "See/Hear \u2192 Tell a Story \u2192 Feel \u2192 Act. Our stories (not facts) drive our emotions."),
            ("Clever Stories", "Victim (\u2018It\u2019s not my fault\u2019), Villain (\u2018It\u2019s all their fault\u2019), Helpless (\u2018There\u2019s nothing I can do\u2019)."),
            ("Retrace Your Path", "When emotions spike, stop and ask: \u2018What am I telling myself?\u2019 Separate facts from stories."),
            ("Useful Story", "Replace the clever story with one that creates emotions that lead to healthy action."),
        ],
        "discussion": "Think of a time your emotions hijacked a conversation. What \u2018clever story\u2019 were you telling yourself? How might you retrace your path to action?",
        "reflection": [
            "Write down a situation that made you angry or frustrated recently.",
            "What story did you tell yourself? Was it a Victim, Villain, or Helpless story?",
            "What are the bare facts\u2014stripped of interpretation?",
        ],
    },
    {
        "num": 6, "title": "Learn to Look", "subtitle": "How to notice when safety is at risk", "part": 2,
        "key_concepts": [
            ("Dual Processing", "Watch the content AND the conditions of the conversation simultaneously."),
            ("Silence", "Masking (sarcasm, sugarcoating), Avoiding (steering away), Withdrawing (pulling out entirely)."),
            ("Violence", "Controlling (forcing views), Labeling (dismissing with stereotypes), Attacking (belittling)."),
            ("Your Style Under Stress", "Everyone defaults to either silence or violence. Know your pattern."),
        ],
        "discussion": "What are your personal warning signs that safety is breaking down in a conversation? Do you tend toward silence or violence under stress?",
        "reflection": [
            "Think of your last heated conversation. Did you notice any signs of silence or violence\u2014in yourself or others?",
            "What is your default: silence or violence?",
            "What physical cues (tight jaw, racing heart, etc.) signal you\u2019re losing safety?",
        ],
    },
    {
        "num": 7, "title": "Make It Safe", "subtitle": "How to make it safe to talk about almost anything", "part": 2,
        "key_concepts": [
            ("Mutual Purpose", "Others feel safe when they believe you care about their goals, not just your own."),
            ("Mutual Respect", "The moment someone feels disrespected, the conversation is no longer about the topic\u2014it\u2019s about dignity."),
            ("Contrasting", "\u2018I don\u2019t want [misunderstanding]. I do want [real intent].\u2019 Fixes misunderstandings fast."),
            ("CRIB", "Commit to seek mutual purpose, Recognize purpose behind the strategy, Invent a mutual purpose, Brainstorm new strategies."),
        ],
        "discussion": "When was the last time you saw a conversation derail because someone felt disrespected? How could Contrasting or CRIB have restored safety?",
        "reflection": [
            "Write a Contrasting statement for a conversation you need to have.",
            "What shared purpose exists between you and the other person?",
            "How could you demonstrate mutual respect even when you disagree?",
        ],
    },
    {
        "num": 8, "title": "STATE My Path", "subtitle": "How to speak persuasively, not abrasively", "part": 2,
        "key_concepts": [
            ("STATE", "Share your facts, Tell your story, Ask for others\u2019 paths, Talk tentatively, Encourage testing."),
            ("Facts First", "Start with the least controversial, most persuasive information\u2014observable facts."),
            ("Tentative Language", "\u2018I\u2019m beginning to wonder if\u2026\u2019 not \u2018You always\u2026\u2019 or \u2018It\u2019s obvious that\u2026\u2019"),
            ("Encourage Testing", "Actively invite disagreement: \u2018What am I missing?\u2019 \u2018Does this match what you see?\u2019"),
        ],
        "discussion": "Practice: Take a difficult message you need to deliver and restructure it using the STATE framework. How does leading with facts change the tone?",
        "reflection": [
            "Think of feedback you need to give. What are the facts (not stories)?",
            "How would you phrase your story tentatively?",
            "Write out your STATE path for this conversation.",
        ],
    },
    {
        "num": 9, "title": "Explore Others\u2019 Paths", "subtitle": "How to listen when others blow up or clam up", "part": 2,
        "key_concepts": [
            ("AMPP", "Ask (to get things rolling), Mirror (confirm feelings), Paraphrase (restate in your own words), Prime (offer your best guess)."),
            ("Curiosity over Defensiveness", "When others go to silence or violence, get curious about their Path to Action."),
            ("ABC", "Agree with what you can, Build where you\u2019d add, Compare where you differ."),
            ("Don\u2019t Push Back", "Resist the urge to rebut. First, fully understand their perspective."),
        ],
        "discussion": "Think of someone who recently clammed up or blew up. What might their Path to Action look like? How could you use AMPP to explore it?",
        "reflection": [
            "Which AMPP skill do you use least? Why?",
            "Practice Priming: \u2018Are you feeling that I don\u2019t value your contribution?\u2019",
            "When someone disagrees with you, do you default to Agree, Build, or Compare?",
        ],
    },
    {
        "num": 10, "title": "Retake Your Pen", "subtitle": "How to be resilient and hear almost anything", "part": 2,
        "key_concepts": [
            ("Retake Your Pen", "You are the author of your own story. Don\u2019t let others write it for you."),
            ("Separate Intent from Impact", "Just because something hurt doesn\u2019t mean harm was intended."),
            ("Natural Consequences", "Let people experience the natural outcomes of their choices instead of shielding or punishing."),
            ("Resilience", "The ability to hear hard feedback without losing your sense of self."),
        ],
        "discussion": "When has someone\u2019s feedback felt like an attack? Looking back, were they writing your story\u2014or were you letting them? How can you \u2018retake your pen\u2019 in future conversations?",
        "reflection": [
            "Think of feedback that stung. What story did you write about yourself because of it?",
            "How would you rewrite that story with more agency?",
            "What\u2019s one area where you\u2019ve given away your pen?",
        ],
    },
    {
        "num": 11, "title": "Move to Action", "subtitle": "How to turn crucial conversations into action and results", "part": 3,
        "key_concepts": [
            ("Decision Methods", "Command, Consult, Vote, Consensus\u2014choose based on who cares, who knows, who must agree, and how many people are involved."),
            ("Who Does What by When", "Every conversation should end with clear assignments: who, what, and a specific deadline."),
            ("Follow Up", "Document decisions and check progress\u2014accountability without micromanagement."),
            ("Avoid Violated Expectations", "Unclear assignments breed resentment. Be explicit."),
        ],
        "discussion": "Think of a meeting that ended with \u2018someone should probably do something about that.\u2019 What happened? How would \u2018Who Does What by When\u2019 have changed the outcome?",
        "reflection": [
            "Which decision method (Command, Consult, Vote, Consensus) do you use most?",
            "After your next conversation, write down the Who/What/When.",
            "How do you follow up without micromanaging?",
        ],
    },
    {
        "num": 12, "title": "Yeah, But", "subtitle": "Advice for tough cases", "part": 3,
        "key_concepts": [
            ("Power Imbalance", "When talking to someone with authority, use facts, ask permission, and focus on mutual purpose."),
            ("Sensitive Topics", "Start with safety, use Contrasting, and stick to observable behavior."),
            ("Trust Violations", "Don\u2019t pretend trust exists when it doesn\u2019t. Be honest about what needs to happen to rebuild it."),
            ("Lost Cause?", "Some people aren\u2019t motivated to change\u2014but skills still matter. Use natural consequences."),
        ],
        "discussion": "What\u2019s the toughest \u2018Yeah, But\u2019 scenario you face? Which principle from this chapter could help you navigate it?",
        "reflection": [
            "Identify your toughest conversation partner. What makes it hard?",
            "Which tool (Contrasting, natural consequences, CRIB) would help most?",
            "What\u2019s the first safe step you could take this week?",
        ],
    },
    {
        "num": 13, "title": "Putting It All Together", "subtitle": "Tools for preparing and learning", "part": 3,
        "key_concepts": [
            ("Coaching Model", "Prepare \u2192 Practice \u2192 Perform \u2192 Review. Skill-building is iterative."),
            ("Preparation Worksheet", "Before a crucial conversation: clarify your purpose, gather facts, plan your STATE, anticipate their path."),
            ("Two-Minute Drill", "Mentally rehearse the first two minutes of the conversation\u2014the opening sets the tone."),
            ("Lifelong Practice", "Mastery comes from repeated application, not one-time reading."),
        ],
        "discussion": "Looking back at this entire course, which single skill or concept will make the biggest difference in your life? How will you practice it this week?",
        "reflection": [
            "Rank the skills from this course: which do you do best? Which needs the most work?",
            "Write out a preparation plan for your next crucial conversation.",
            "Who will be your accountability partner for practicing these skills?",
        ],
    },
]

PART_LABELS = {
    1: "Part I \u2014 Before You Open Your Mouth",
    2: "Part II \u2014 How to Open Your Mouth",
    3: "Part III \u2014 How to Finish",
}

def generate_handout(ch, prev_ch, next_ch):
    e = html.escape
    concepts_html = ""
    for term, defn in ch["key_concepts"]:
        concepts_html += f"""            <div class="concept">
                <div class="concept-term">{e(term)}</div>
                <div class="concept-def">{e(defn)}</div>
            </div>\n"""

    reflection_html = "\n".join(f"            <li>{e(r)}</li>" for r in ch["reflection"])

    prev_btn = f'<a href="chapter_{prev_ch["num"]:02d}.html" class="nav-btn">&#x25C0; Ch. {prev_ch["num"]}</a>' if prev_ch else '<span class="nav-btn disabled">&#x25C0; Prev</span>'
    next_btn = f'<a href="chapter_{next_ch["num"]:02d}.html" class="nav-btn">Ch. {next_ch["num"]} &#x25B6;</a>' if next_ch else '<span class="nav-btn disabled">Next &#x25B6;</span>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter {ch["num"]} Handout \u2014 {e(ch["title"])}</title>
    <style>
        :root {{
            --brand-red: #e30613;
            --brand-red-accessible: #c20510;
            --text-dark: #333;
            --text-light: #666;
            --bg-light: #f8f9fa;
            --border-color: #ddd;
            --blue: #4a90e2;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: var(--text-dark);
            line-height: 1.6;
            background: white;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 30px 80px;
        }}
        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: var(--blue);
            text-decoration: none;
            font-weight: 600;
        }}
        .back-link:hover {{ text-decoration: underline; }}
        header {{
            text-align: center;
            margin-bottom: 32px;
            padding-bottom: 20px;
            border-bottom: 3px solid var(--brand-red);
        }}
        header .chapter-num {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--brand-red);
            font-weight: 700;
        }}
        header h1 {{
            font-size: 1.8rem;
            color: var(--brand-red-accessible);
            margin: 6px 0 4px;
        }}
        header .subtitle {{
            font-size: 1.05rem;
            color: var(--text-light);
            font-style: italic;
        }}
        .part-badge {{
            display: inline-block;
            font-size: 0.75rem;
            background: var(--bg-light);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 3px 12px;
            color: var(--text-light);
            margin-top: 8px;
        }}
        h2 {{
            color: var(--brand-red-accessible);
            font-size: 1.3rem;
            margin: 28px 0 14px;
            padding-bottom: 6px;
            border-bottom: 2px solid var(--bg-light);
        }}
        .concepts-grid {{
            display: grid;
            gap: 12px;
        }}
        .concept {{
            background: var(--bg-light);
            border-radius: 8px;
            padding: 14px 18px;
            border-left: 4px solid var(--brand-red);
        }}
        .concept-term {{
            font-weight: 700;
            color: var(--brand-red-accessible);
            font-size: 0.95rem;
            margin-bottom: 4px;
        }}
        .concept-def {{
            font-size: 0.92rem;
            color: var(--text-dark);
        }}
        .discussion-box {{
            background: #fff8e1;
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 18px 20px;
            margin: 16px 0;
        }}
        .discussion-box .label {{
            font-weight: 700;
            color: #e65100;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }}
        .reflection-list {{
            list-style: none;
            counter-reset: refl;
        }}
        .reflection-list li {{
            counter-increment: refl;
            padding: 10px 14px 10px 44px;
            position: relative;
            margin-bottom: 8px;
            background: var(--bg-light);
            border-radius: 8px;
            font-size: 0.95rem;
        }}
        .reflection-list li::before {{
            content: counter(refl);
            position: absolute;
            left: 14px;
            top: 10px;
            width: 22px;
            height: 22px;
            background: var(--brand-red);
            color: white;
            border-radius: 50%;
            font-size: 0.75rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .write-area {{
            border: 1px dashed var(--border-color);
            border-radius: 8px;
            min-height: 100px;
            margin: 12px 0;
            padding: 12px;
            background: var(--bg-light);
            font-size: 0.85rem;
            color: var(--text-light);
            text-align: center;
            line-height: 100px;
        }}
        .print-btn {{
            display: inline-block;
            margin-left: 16px;
            padding: 6px 14px;
            background: var(--bg-light);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-dark);
            font-size: 0.85rem;
            cursor: pointer;
        }}
        .print-btn:hover {{ background: var(--border-color); }}
        .nav-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid var(--border-color);
            gap: 12px;
        }}
        .nav-btn {{
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
        }}
        .nav-btn:hover {{ background: var(--brand-red-accessible); transform: translateY(-1px); color: white; text-decoration: none; }}
        .nav-btn.secondary {{ background: #555; }}
        .nav-btn.secondary:hover {{ background: #333; }}
        .nav-btn.disabled {{ opacity: 0.35; pointer-events: none; }}
        @media print {{
            .back-link, .nav-footer, .print-btn {{ display: none; }}
            body {{ padding: 20px; max-width: 100%; }}
            .concept {{ break-inside: avoid; }}
        }}
    </style>
</head>
<body>
    <a href="index.html" class="back-link">&larr; All Handouts</a>
    <button class="print-btn" onclick="window.print()">&#x1f5a8; Print</button>
    <header>
        <div class="chapter-num">Chapter {ch["num"]} Handout</div>
        <h1>{e(ch["title"])}</h1>
        <div class="subtitle">{e(ch["subtitle"])}</div>
        <div class="part-badge">{e(PART_LABELS[ch["part"]])}</div>
    </header>

    <h2>Key Concepts</h2>
    <div class="concepts-grid">
{concepts_html}    </div>

    <h2>Discussion Question</h2>
    <div class="discussion-box">
        <div class="label">Whole-Group Discussion</div>
        <p>{e(ch["discussion"])}</p>
    </div>

    <h2>Personal Reflection</h2>
    <ol class="reflection-list">
{reflection_html}
    </ol>

    <h2>Notes</h2>
    <div class="write-area">Use this space for your notes (print-friendly)</div>

    <nav class="nav-footer">
        {prev_btn}
        <a href="index.html" class="nav-btn secondary">All Handouts</a>
        {next_btn}
    </nav>
</body>
</html>
"""

os.makedirs(OUT_DIR, exist_ok=True)

for i, ch in enumerate(CHAPTERS):
    prev_ch = CHAPTERS[i - 1] if i > 0 else None
    next_ch = CHAPTERS[i + 1] if i < len(CHAPTERS) - 1 else None
    fname = f"chapter_{ch['num']:02d}.html"
    path = os.path.join(OUT_DIR, fname)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(generate_handout(ch, prev_ch, next_ch))
    print(f"  \u2713 {fname}")

print(f"\nGenerated {len(CHAPTERS)} handout pages")
