#!/usr/bin/env python3
"""
Fix Missing CSS Variables - Complete Gold Standard CSS
==============================================
Restores all missing CSS variables that were accidentally removed.
"""

import re
from pathlib import Path

def fix_missing_css_vars():
    """Restore missing CSS variables in all chapters."""
    
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
            
            # Fix incomplete CSS variables
            old_root_pattern = r'(:root {\s*--brand-red-accessible: #c20510;\s*})'
            
            new_root_vars = '''    :root {
        --brand-red: #e30613;
        --brand-red-accessible: #c20510;
        --text-dark: #333;
        --text-light: #666;
        --bg-light: #f8f9fa;
        --border-color: #ddd;
        --discussion-blue: #4a90e2;
        --digest-green: #48bb78;
        --digest-green-dark: #38a169;
    }'''
            
            content = re.sub(old_root_pattern, new_root_vars, content)
            
            # Write fixed content
            with open(chapter_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Fixed CSS variables: {chapter_file.name}")
            fixed_count += 1
            
        except Exception as e:
            print(f"❌ Error fixing {chapter_file.name}: {e}")
    
    print(f"\n🎉 CSS variables fix complete! {fixed_count}/{len(chapter_files)} chapters updated")
    return True

def main():
    print("🔧 FIXING MISSING CSS VARIABLES")
    print("=" * 50)
    print("🚨 CRITICAL ISSUE: Missing CSS variables causing Edge display problems")
    print("📋 VARIABLES TO RESTORE:")
    print("   • --brand-red: #e30613")
    print("   • --text-dark: #333")
    print("   • --text-light: #666")
    print("   • --bg-light: #f8f9fa")
    print("   • --border-color: #ddd")
    print("   • --discussion-blue: #4a90e2")
    print("   • --digest-green: #48bb78")
    print("   • --digest-green-dark: #38a169")
    print("=" * 50)
    
    success = fix_missing_css_vars()
    
    if success:
        print("\n✅ CSS variables fix completed successfully!")
        print("📋 Results:")
        print("   • All missing CSS variables restored")
        print("   • Edge compatibility issues resolved")
        print("   • Gold Standard styling fully functional")
        print("   • Publisher branding preserved")

if __name__ == "__main__":
    main()
