#!/usr/bin/env python3
"""
Generate free preview versions of each chapter (first ~2,000 words).
Adds a paywall teaser at the end.
"""
import os
import re

SOURCE_DIR = os.path.expanduser("~/Desktop/claude-code-book")
OUTPUT_DIR = os.path.expanduser("~/Desktop/claude-unleashed-repo/preview")
GUMROAD_LINK = "https://phy041.gumroad.com/l/claude-unleashed"
PREVIEW_WORDS = 2000

TEASER = """

---

## ✋ You've reached the end of the free preview

This is **{pct}%** of *{title}*.

The full chapter is **{total_words:,} words** — {remaining_words:,} more words covering:

{remaining_sections}

### Get the Complete Book

**[Claude Unleashed: The Complete Guide to Building With Claude Code]({gumroad})**

- 495,000+ words across 18 chapters + 7 appendices
- Source code citations from all 510,000 lines of leaked Claude Code
- Real stories, real numbers, real techniques
- Free updates forever

**$29.99** (or pay what you want, minimum $19.99)

→ **[Buy on Gumroad]({gumroad})**

---

*Already bought it? Check your email for the download link.*
"""

CHAPTER_TITLES = {
    "00_preface.md": "Preface: The Leak Story",
    "01_what_is_claude_code.md": "Chapter 1: What Is Claude Code, Really?",
    "02_the_memory_garden.md": "Chapter 2: The Memory Garden",
    "03_fifty_transformations.md": "Chapter 3: Fifty Transformations",
    "04_rate_limit_survival.md": "Chapter 4: The Rate Limit Survival Guide",
    "05_settings_that_change_everything.md": "Chapter 5: The Settings That Change Everything",
    "06_shipping_with_an_ai_team.md": "Chapter 6: Shipping Products With an AI Team",
    "07_510k_lines_of_brilliance.md": "Chapter 7: 510,000 Lines of Brilliance",
    "08_building_on_the_platform.md": "Chapter 8: Building on the Platform",
    "09_when_everyone_can_build.md": "Chapter 9: When Everyone Can Build",
    "10_a_love_letter.md": "Chapter 10: A Love Letter",
    "appendix_a_settings_json.md": "Appendix A: Complete settings.json Reference",
    "appendix_b_feature_flags.md": "Appendix B: 80+ Feature Flags Decoded",
    "appendix_c_buddy_species.md": "Appendix C: All 18 Buddy Species",
    "appendix_d_claude_md_templates.md": "Appendix D: CLAUDE.md Templates",
    "appendix_e_architecture_map.md": "Appendix E: Architecture Map",
    "appendix_f_cost_calculator.md": "Appendix F: Cost Calculator",
    "appendix_g_hidden_commands.md": "Appendix G: Hidden Commands Catalog",
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename, title in CHAPTER_TITLES.items():
    src = os.path.join(SOURCE_DIR, filename)
    if not os.path.exists(src):
        print(f"SKIP {filename} (not found)")
        continue

    with open(src, "r") as f:
        content = f.read()

    words = content.split()
    total_words = len(words)
    preview_words = min(PREVIEW_WORDS, total_words)

    # Find a clean paragraph break near PREVIEW_WORDS
    preview_text = " ".join(words[:preview_words])
    # Snap to last paragraph break
    last_para = preview_text.rfind("\n\n")
    if last_para > len(preview_text) * 0.7:
        preview_text = preview_text[:last_para]

    # Find remaining section headings for the teaser
    remaining_content = content[len(preview_text):]
    headings = re.findall(r'^#{1,3} .+', remaining_content, re.MULTILINE)
    top_headings = headings[:6]
    remaining_sections = "\n".join(f"- {h.lstrip('#').strip()}" for h in top_headings)
    if len(headings) > 6:
        remaining_sections += f"\n- *...and {len(headings) - 6} more sections*"

    pct = round(preview_words / total_words * 100)
    remaining_words = total_words - len(preview_text.split())

    teaser_filled = TEASER.format(
        pct=pct,
        title=title,
        total_words=total_words,
        remaining_words=remaining_words,
        remaining_sections=remaining_sections or "- The rest of the chapter",
        gumroad=GUMROAD_LINK,
    )

    output = preview_text + teaser_filled
    out_path = os.path.join(OUTPUT_DIR, filename)
    with open(out_path, "w") as f:
        f.write(output)

    print(f"✓ {filename}: {preview_words}/{total_words} words ({pct}%)")

print("\nAll preview files generated.")
