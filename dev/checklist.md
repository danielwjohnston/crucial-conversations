# Promotion Checklist — shared.js to Production

## Pre-promotion testing

- [ ] Open `dev/test_chapter_12.html` in Chrome, Firefox, Safari
- [ ] Verify slide navigation (arrow keys, buttons, Home/End)
- [ ] Verify chapter dropdown opens, highlights current chapter, navigates
- [ ] Verify auto-advance timer (press 'A') with countdown circle
- [ ] Verify digest modals open/close (press 'D' on discussion slides, click backdrop)
- [ ] Verify deep linking: `?slide=5`, `?slide=last`
- [ ] Verify term tooltips on hover and focus
- [ ] Verify chapter boundary navigation (Next on last slide → next chapter)
- [ ] Verify mobile responsive layout
- [ ] Verify keyboard: Escape closes modals/dropdown
- [ ] Compare behavior side-by-side with `../slidedecks/chapter_12_yeah_but.html`

## Promotion steps

1. **Copy `shared.js`** to `slidedecks/shared.js`

2. **For each of the 13 chapter files** in `slidedecks/`:
   - Find the `<script>` tag containing the inline JS (starts after `</nav>`)
   - Keep only the chapter-specific config:
     ```html
     <script>
         const CURRENT_CHAPTER_INDEX = N;  // 0-based
         const DURATIONS_SECONDS = [...];
     </script>
     <script src="shared.js"></script>
     ```
   - Remove all other inline JS (CHAPTERS array through the tooltip IIFE)

3. **Chapter index reference:**

   | File | CURRENT_CHAPTER_INDEX |
   |------|-----------------------|
   | chapter_01_crucial_conversation.html | 0 |
   | chapter_02_mastering_conversations.html | 1 |
   | chapter_03_choose_topic.html | 2 |
   | chapter_04_start_heart.html | 3 |
   | chapter_05_master_stories.html | 4 |
   | chapter_06_learn_to_look.html | 5 |
   | chapter_07_make_safe.html | 6 |
   | chapter_08_state_path.html | 7 |
   | chapter_09_explore_paths.html | 8 |
   | chapter_10_retake_pen.html | 9 |
   | chapter_11_move_action.html | 10 |
   | chapter_12_yeah_but.html | 11 |
   | chapter_13_putting_together.html | 12 |

4. **Test each chapter** after conversion (at minimum: slides, dropdown, keyboard)

5. **Update `templates/slidedeck_template.html`** to use the shared.js pattern

6. **Commit** with message: `refactor: extract shared JS engine to slidedecks/shared.js`

## Rollback

If issues are found after promotion:

- `git revert` the commit
- Production slidedecks still have their inline JS as backup in git history
- The `dev/` folder remains as reference
