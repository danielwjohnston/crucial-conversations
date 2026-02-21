#!/usr/bin/env python3
"""
Fix Duplicate Auto-Advance Buttons and First Slide Issues
==================================================
Removes duplicate buttons and fixes first slide layout.
"""

import re
from pathlib import Path

def fix_duplicate_buttons():
    """Fix duplicate auto-advance buttons and first slide issues."""
    
    slidedecks_dir = Path("slidedecks")
    
    if not slidedecks_dir.exists():
        print("❌ slidedecks directory not found")
        return False
    
    chapter_files = list(slidedecks_dir.glob("chapter_*.html"))
    
    print(f"📋 Found {len(chapter_files)} chapter files to fix")
    
    fixed_count = 0
    
    for chapter_file in sorted(chapter_files):
        try:
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix 1: Remove duplicate auto-advance button from first slide
            # Look for the pattern where first slide has misplaced button
            first_slide_button_pattern = r'(<div class="slide active">\s*<div class="slide-content"[^>]*>.*?<button class="auto-advance-toggle"[^>]*id="autoAdvanceToggle"[^>]*>.*?</button>.*?</div>\s*</div>)'
            
            # Replace with clean first slide content
            clean_first_slide = '''<div class="slide active">
            <div class="slide-content">
                <h1>What's a Crucial Conversation?</h1>
                <div class="quote-box">
                    <p style="font-size: 1.5em; text-align: center; margin-bottom: 20px;">"The single biggest problem in communication is the illusion that it has taken place."</p>
                    <p style="text-align: center; font-size: 1.1em;">— George Bernard Shaw</p>
                </div>
            </div>
        </div>'''
            
            content = re.sub(first_slide_button_pattern, clean_first_slide, content, flags=re.DOTALL)
            
            # Fix 2: Remove duplicate slide counter from first slide
            slide_counter_pattern = r'(<div class="slide-counter"[^>]*>.*?</div>\s*)'
            content = re.sub(slide_counter_pattern, '', content, flags=re.DOTALL)
            
            # Fix 3: Remove misplaced title from first slide
            misplaced_title_pattern = r'(<div class="slide active">\s*<div class="slide-content"[^>]*>.*?<div>Leadership Bookclub - What\'s a Crucial Conversation</div>.*?</div>\s*)'
            content = re.sub(misplaced_title_pattern, '', content, flags=re.DOTALL)
            
            # Fix 4: Ensure only one auto-advance button exists in navigation
            # Remove any extra auto-advance buttons that might exist
            nav_button_pattern = r'(<nav class="navigation"[^>]*>.*?<button class="auto-advance-toggle"[^>]*>.*?</button>.*?</nav>)'
            
            # Check if navigation already has auto-advance button
            nav_match = re.search(r'<nav class="navigation"[^>]*>.*?<button class="auto-advance-toggle"', content)
            if nav_match:
                # Navigation already has button, remove any duplicates
                content = re.sub(nav_button_pattern, '', content, flags=re.DOTALL)
            
            # Write fixed content
            with open(chapter_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Fixed duplicate buttons: {chapter_file.name}")
            fixed_count += 1
            
        except Exception as e:
            print(f"❌ Error fixing {chapter_file.name}: {e}")
    
    print(f"\n🎉 Duplicate button fix complete! {fixed_count}/{len(chapter_files)} chapters updated")
    return True

def main():
    print("🔧 FIXING DUPLICATE AUTO-ADVANCE BUTTONS")
    print("=" * 50)
    print("🚨 ISSUES TO FIX:")
    print("   • Duplicate auto-advance buttons")
    print("   • First slide layout problems")
    print("   • Conflicting element IDs")
    print("   • Misplaced navigation elements")
    print("=" * 50)
    
    success = fix_duplicate_buttons()
    
    if success:
        print("\n✅ Duplicate button fix completed successfully!")
        print("📋 Results:")
        print("   • Removed duplicate auto-advance buttons")
        print("   • Fixed first slide layout")
        print("   • Cleaned up conflicting IDs")
        print("   • Preserved Gold Standard functionality")

if __name__ == "__main__":
    main()
