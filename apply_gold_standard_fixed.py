#!/usr/bin/env python3
"""
Crucial Conversations Gold Standard Upgrader - FIXED VERSION
=============================================================
Applies the Chapter 10 gold standard features to all chapters.
Preserves all existing content while adding enhancements.
"""

import re
import os
import sys
import argparse
from pathlib import Path

# Chapter metadata
CHAPTERS = {
    "chapter_01": {"num": "1", "title": "What's a Crucial Conversation", "title_upper": "WHAT'S A CRUCIAL CONVERSATION", "subtitle": "And who cares?"},
    "chapter_02": {"num": "2", "title": "Mastering Crucial Conversations", "title_upper": "MASTERING CRUCIAL CONVERSATIONS", "subtitle": "The power of dialogue"},
    "chapter_03": {"num": "3", "title": "Choose Your Topic", "title_upper": "CHOOSE YOUR TOPIC", "subtitle": "How to be sure you hold the right conversation"},
    "chapter_04": {"num": "4", "title": "Start with Heart", "title_upper": "START WITH HEART", "subtitle": "How to stay focused on what you really want"},
    "chapter_05": {"num": "5", "title": "Master My Stories", "title_upper": "MASTER MY STORIES", "subtitle": "How to stay in dialogue when you're angry, scared, or hurt"},
    "chapter_06": {"num": "6", "title": "Learn to Look", "title_upper": "LEARN TO LOOK", "subtitle": "How to notice when safety is at risk"},
    "chapter_07": {"num": "7", "title": "Make It Safe", "title_upper": "MAKE IT SAFE", "subtitle": "How to make it safe to talk about almost anything"},
    "chapter_08": {"num": "8", "title": "STATE My Path", "title_upper": "STATE MY PATH", "subtitle": "How to speak persuasively, not abrasively"},
    "chapter_09": {"num": "9", "title": "Explore Others' Paths", "title_upper": "EXPLORE OTHERS' PATHS", "subtitle": "How to listen when others blow up or clam up"},
    "chapter_10": {"num": "10", "title": "Retake Your Pen", "title_upper": "RETAKE YOUR PEN", "subtitle": "How to be resilient and hear almost anything"},
    "chapter_11": {"num": "11", "title": "Move to Action", "title_upper": "MOVE TO ACTION", "subtitle": "How to turn crucial conversations into action and results"},
    "chapter_12": {"num": "12", "title": "Yeah, But", "title_upper": "YEAH, BUT", "subtitle": "Advice for tough cases"},
    "chapter_13": {"num": "13", "title": "Putting It All Together", "title_upper": "PUTTING IT ALL TOGETHER", "subtitle": "Tools for preparing and learning"},
}

def extract_slide_content(html_content):
    """Extract slide content from existing HTML."""
    # Find all slide divs with their content
    slide_pattern = r'<div class="slide(?:[^"]*)"[^>]*>(.*?)</div>\s*(?=</div>\s*$|<div class="slide|$)'
    slides = re.findall(slide_pattern, html_content, re.DOTALL)
    return slides

def detect_slide_types(slides):
    """Auto-detect slide types for duration assignment."""
    durations = []
    
    for i, slide in enumerate(slides):
        slide_lower = slide.lower()
        duration = 90  # Default
        
        # Title slide
        if i == 0:
            duration = 30
        # Discussion slides
        elif 'discussion-slide' in slide_lower or 'discussion question' in slide_lower:
            # Look for time indicators
            time_match = re.search(r'take\s+(\d+)[-–](\d+)\s+minutes', slide_lower)
            if time_match:
                minutes = int(time_match.group(1))
                duration = minutes * 60
            else:
                duration = 300  # 5 minutes default for discussion
        # Dan's Digest slides
        elif 'dans-digest-slide' in slide_lower or "dan's digest" in slide_lower:
            duration = 120
        # Exercise slides
        elif 'exercise' in slide_lower or 'activity' in slide_lower:
            duration = 120
        # Summary slides
        elif 'key takeaway' in slide_lower or 'summary' in slide_lower:
            duration = 90
        # Transition slides
        elif 'coming up next' in slide_lower or 'preview' in slide_lower:
            duration = 60
            
        durations.append(duration)
    
    return durations

def generate_durations_array(slides):
    """Generate the DURATIONS_SECONDS array."""
    durations = detect_slide_types(slides)
    
    array_lines = ["        const DURATIONS_SECONDS = ["]
    for i, duration in enumerate(durations):
        comment = f"  // {i+1} "
        if i == 0:
            comment += "Title"
        elif "discussion" in slides[i].lower():
            comment += "Discussion"
        elif "dan's digest" in slides[i].lower():
            comment += "Dan's Digest"
        elif "exercise" in slides[i].lower():
            comment += "Exercise"
        else:
            comment += "Content"
        
        array_lines.append(f"            {duration}, {comment}")
    
    array_lines.append("        ];")
    return "\n".join(array_lines)

def apply_gold_standard(chapter_key, input_file, output_file, dry_run=False):
    """Apply gold standard template to a chapter."""
    try:
        # Read existing content
        with open(input_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Extract slide content
        slides = extract_slide_content(original_content)
        
        if not slides:
            print(f"Warning: No slides found in {input_file}")
            return False
        
        # Read gold standard template (from Chapter 10)
        template_path = Path("original_files/chapter10_slideshow.html")
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Get chapter metadata
        chapter_info = CHAPTERS.get(chapter_key, {})
        
        # Replace placeholders in template
        new_content = template_content
        new_content = new_content.replace("Leadership Bookclub - Retake Your Pen", f"Leadership Bookclub - {chapter_info.get('title', '')}")
        new_content = new_content.replace("RETAKE YOUR PEN", chapter_info.get('title_upper', ''))
        new_content = new_content.replace("Chapter 10", f"Chapter {chapter_info.get('num', '')}")
        new_content = new_content.replace("How to be resilient and hear almost anything", chapter_info.get('subtitle', ''))
        
        # Update persistent header
        new_content = re.sub(
            r'<h2>RETAKE YOUR PEN</h2>',
            f'<h2>{chapter_info.get("title_upper", "")}</h2>',
            new_content
        )
        new_content = re.sub(
            r'<p>Chapter 10 &bull; How to be resilient and hear almost anything</p>',
            f'<p>Chapter {chapter_info.get("num", "")} &bull; {chapter_info.get("subtitle", "")}</p>',
            new_content
        )
        
        # Generate durations array
        durations_array = generate_durations_array(slides)
        
        # Replace slide content in template
        # Find the main content area and replace slides
        main_content_pattern = r'<main id="main-content" class="slideshow-container".*?</main>'
        main_match = re.search(main_content_pattern, template_content, re.DOTALL)
        
        if main_match:
            # Build new main content
            new_main = '<main id="main-content" class="slideshow-container" aria-label="Slideshow presentation">\n'
            
            # Add slides
            for i, slide in enumerate(slides):
                # Determine slide classes
                slide_classes = ["slide"]
                if i == 0:
                    slide_classes.append("title-slide")
                elif "discussion-slide" in slide.lower() or "discussion question" in slide.lower():
                    slide_classes.append("discussion-slide")
                elif "dans-digest-slide" in slide.lower() or "dan's digest" in slide.lower():
                    slide_classes.append("dans-digest-slide")
                
                new_main += f'        <div class="{" ".join(slide_classes)}">\n'
                new_main += slide.strip()
                new_main += '\n        </div>\n\n'
            
            new_main += '</main>'
            
            # Replace the main content
            new_content = re.sub(main_content_pattern, new_main, new_content, flags=re.DOTALL)
        
        # Replace durations array
        new_content = re.sub(
            r'const DURATIONS_SECONDS = \[.*?\];',
            durations_array,
            new_content,
            flags=re.DOTALL
        )
        
        # Update total slides count
        new_content = re.sub(
            r'const totalSlides = slides\.length;',
            f'const totalSlides = {len(slides)};',
            new_content
        )
        
        # Update slide counter initialization
        new_content = re.sub(
            r'document\.getElementById\("totalSlides"\)\.textContent = totalSlides;',
            f'document.getElementById("totalSlides").textContent = {len(slides)};',
            new_content
        )
        
        if dry_run:
            print(f"Would upgrade {input_file}:")
            print(f"  - Found {len(slides)} slides")
            print(f"  - Generated {len(durations_array.splitlines())} duration entries")
            return True
        
        # Write upgraded content
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Upgraded {input_file} → {output_file}")
        print(f"   - {len(slides)} slides processed")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {input_file}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Apply Gold Standard to Crucial Conversations chapters")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    parser.add_argument("--input-dir", default="slidedecks", help="Input directory")
    parser.add_argument("--output-dir", default="slidedecks", help="Output directory")
    
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    # Create output directory if different
    if args.output_dir != args.input_dir:
        output_dir.mkdir(exist_ok=True)
    
    # Find all chapter files
    chapter_files = {}
    for file_path in input_dir.glob("chapter_*.html"):
        # Extract chapter number from filename
        match = re.search(r'chapter_(\d+)', file_path.name.lower())
        if match:
            chapter_num = match.group(1).zfill(2)
            chapter_key = f"chapter_{chapter_num}"
            chapter_files[chapter_key] = file_path
    
    print(f"Found {len(chapter_files)} chapter files")
    
    success_count = 0
    for chapter_key, input_file in sorted(chapter_files.items()):
        if args.output_dir == args.input_dir:
            output_file = input_file
        else:
            output_file = output_dir / input_file.name
        
        if apply_gold_standard(chapter_key, input_file, output_file, args.dry_run):
            success_count += 1
    
    if args.dry_run:
        print(f"\n🔍 Dry run completed. {success_count} files ready for upgrade.")
        print("Run without --dry-run to apply changes.")
    else:
        print(f"\n🎉 Upgrade completed! {success_count} files upgraded to Gold Standard.")
        print("\nNext steps:")
        print("1. Test a few chapters in your browser")
        print("2. Verify timing and functionality")
        print("3. Commit changes to version control")

if __name__ == "__main__":
    main()
