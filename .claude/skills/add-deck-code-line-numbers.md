---
name: add-deck-code-line-numbers
description: Add source file line number references to code blocks in Reveal.js deck slides
---

# Add Line Numbers to Deck Code Blocks

When you have code snippets in deck slides (e.g., `lab5-deck/sections/*/slides.html`), link them to their source files with both a reference range and left-margin line numbers.

## Process

### 1. Identify the code block and its source
- Locate the `<div class="code-block">` containing the code snippet
- Find where this code actually lives in the repo (e.g., `labs/lab5/orchestrate.py:287–318`)
- Note the exact line number range from the source file

### 2. Update the code-label
Change the `<p class="code-label">` to include the line range:

**Before:**
```html
<p class="code-label">labs/lab5/orchestrate.py</p>
```

**After:**
```html
<p class="code-label">labs/lab5/orchestrate.py · 287–318</p>
```

Use the en-dash `·` (not hyphen) and format as `· START–END`.

### 3. Add Reveal.js line number attributes
Add `data-line-numbers` and `data-start="LINE_NUMBER"` to the `<pre><code>` tag:

**Before:**
```html
<pre><code>def classify_complexity(book: FailedBook) -> Complexity:
```

**After:**
```html
<pre><code data-line-numbers data-start="287">def classify_complexity(book: FailedBook) -> Complexity:
```

The `data-start` value should match the **first line number** of your code block in the source file.

### 4. Rebuild all decks
After editing `slides.html` files, regenerate all deck `index.html` files:

```bash
cd training-materials/staging
python3 scripts/build_deck.py
```

This ensures the fragments are properly compiled into the generated index.html files.

## Verify the changes
Check that the code-label shows the line range and that `data-line-numbers` was compiled into `index.html`:

```bash
grep "code-label" training-materials/staging/lab5-deck/index.html
grep "data-line-numbers" training-materials/staging/lab5-deck/index.html
```

## Key details

- **code-label format:** File path + `·` + line range (e.g., `labs/lab5/orchestrate.py · 287–318`)
- **data-start value:** The starting line number (integer, no dashes)
- **data-line-numbers:** Required attribute; no value needed (Reveal.js auto-enables)
- **en-dash:** Use `·` (U+00B7, MIDDLE DOT) between filename and range, not a hyphen
- **Always rebuild:** Changes to `slides.html` won't appear until `build_deck.py` regenerates `index.html`

## Example workflow

```bash
# 1. Edit the slides.html file
# Add line range to code-label and data-line-numbers attributes to code blocks

# 2. Rebuild all decks
cd training-materials/staging
python3 scripts/build_deck.py

# 3. Verify in browser (hard refresh: Cmd+Shift+R or Ctrl+Shift+R)
# Check that line numbers appear on the left margin of code blocks
```
