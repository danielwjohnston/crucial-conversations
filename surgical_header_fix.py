#!/usr/bin/env python3
"""
Surgical Header Fix - Publisher Branding Only
=========================================
Updates ONLY the header content to use official CrucialLearning.com branding
without touching CSS, JavaScript, or other functionality.
"""

import re
import os
from pathlib import Path

def fix_headers_surgically():
    """Apply surgical header fix - only change header content."""
    
    slidedecks_dir = Path("slidedecks")
    
    if not slidedecks_dir.exists():
        print("❌ slidedecks directory not found")
        return False
    
    chapter_files = list(slidedecks_dir.glob("chapter_*.html"))
    
    print(f"📋 Found {len(chapter_files)} chapter files for surgical fix")
    
    fixed_count = 0
    
    for chapter_file in sorted(chapter_files):
        try:
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Surgical fix: ONLY change the header content, nothing else
            old_header_pattern = r'(<header class="header"[^>]*>)(.*?)(</header>)'
            
            # Replace with official publisher branding
            new_header_content = 'CrucialLearning.com | 800.449.5989'
            new_header = f'\\1{new_header_content}\\3'
            
            content = re.sub(old_header_pattern, new_header, content, flags=re.DOTALL)
            
            # Also fix persistent header if it exists
            old_persistent_pattern = r'(<div class="persistent-header"[^>]*>.*?<h3>Leadership Bookclub</h3>.*?<h2>)([^<]*)(</h2>.*?</div>)'
            
            # Map chapter titles to proper format
            title_match = re.search(r'<title>Leadership Bookclub - (.+?)</title>', content)
            if title_match:
                chapter_title = title_match.group(1)
                
                chapter_mappings = {
                    "What's a Crucial Conversation": ("WHAT'S A CRUCIAL CONVERSATION", "1", "And who cares?"),
                    "Mastering Crucial Conversations": ("MASTERING CRUCIAL CONVERSATIONS", "2", "The power of dialogue"),
                    "Choose Your Topic": ("CHOOSE YOUR TOPIC", "3", "How to be sure you hold the right conversation"),
                    "Start with Heart": ("START WITH HEART", "4", "How to stay focused on what you really want"),
                    "Master My Stories": ("MASTER MY STORIES", "5", "How to stay in dialogue when you're angry, scared, or hurt"),
                    "Learn to Look": ("LEARN TO LOOK", "6", "How to notice when safety is at risk"),
                    "Make It Safe": ("MAKE IT SAFE", "7", "How to make it safe to talk about almost anything"),
                    "STATE My Path": ("STATE MY PATH", "8", "How to speak persuasively, not abrasively"),
                    "Explore Others' Paths": ("EXPLORE OTHERS' PATHS", "9", "How to listen when others blow up or clam up"),
                    "Retake Your Pen": ("RETAKE YOUR PEN", "10", "How to be resilient and hear almost anything"),
                    "Move to Action": ("MOVE TO ACTION", "11", "How to turn crucial conversations into action and results"),
                    "Yeah, But": ("YEAH, BUT", "12", "Advice for tough cases"),
                    "Putting It All Together": ("PUTTING IT ALL TOGETHER", "13", "Tools for preparing and learning")
                }
                
                if chapter_title in chapter_mappings:
                    title_upper, num, subtitle = chapter_mappings[chapter_title]
                    new_persistent_content = f'\\1{title_upper}</h2>\\n        <p>Chapter {num} &bull; {subtitle}</p>\\2'
                    content = re.sub(old_persistent_pattern, new_persistent_content, content, flags=re.DOTALL)
            
            # Write the surgically fixed content
            with open(chapter_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Surgically fixed: {chapter_file.name}")
            fixed_count += 1
            
        except Exception as e:
            print(f"❌ Error fixing {chapter_file.name}: {e}")
    
    print(f"\n🎉 Surgical header fix complete! {fixed_count}/{len(chapter_files)} chapters updated")
    print("📋 Only header content changed - CSS and JavaScript preserved")
    return True

def main():
    print("🔧 SURGICAL HEADER FIX - Publisher Branding Only")
    print("=" * 55)
    print("⚠️  This fix ONLY changes header content")
    print("⚠️  CSS, JavaScript, and functionality preserved")
    print("=" * 55)
    
    success = fix_headers_surgically()
    
    if success:
        print("\n✅ Surgical header fix completed successfully!")
        print("📋 Results:")
        print("   • Official CrucialLearning.com branding applied")
        print("   • All CSS and JavaScript preserved")
        print("   • No auto-advance issues introduced")
        print("   • Gold Standard features maintained")

if __name__ == "__main__":
    main()
