---
name: fix-python-code-coloring
description: Audit and fix Python code block syntax highlighting across training decks
---

# Fix Python Code Block Syntax Highlighting

## Purpose
Ensure all Python code blocks in training deck slides (Lab 1–8) display with consistent, readable syntax highlighting using the `vscode-dark-modern` theme and highlight.js.

## When to Use
Invoke this skill when:
- Raw markup such as `<span class="cm">` is **visible as text** on the rendered slide
- A code block is displaying plain white text with minimal coloring
- Keywords are colored but identifiers, constants, or strings are not
- Manual `<span class="cm">` wrappers exist around comments or code elements
- A new Python code example is added to a deck slide

## Why the spans become visible

When a `<code>` tag carries `class="language-python"`, highlight.js parses and
replaces the element's inner HTML, so any hand-written `<span>` is consumed
harmlessly. When the language class is **missing**, highlight.js escapes the
content instead, and the literal text `<span class="cm">` renders on the slide.

The two defects therefore always travel together. Fix both at once:
1. Add `class="language-python"` to the `<code>` tag.
2. Delete every manual `<span class="cm">...</span>` wrapper.

> `data-line-numbers` and `data-start="N"` are Reveal.js attributes and are
> unrelated to highlighting. Keep them; they coexist with the language class:
> `<code class="language-python" data-line-numbers data-start="296">`

## Process

### 1. Locate the Issue
- Run the deck locally and navigate to the slide with the code block
- Verify that keywords (`if`, `elif`, `class`, `def`) ARE colored but other elements are NOT
- Check the source HTML in the slide's `.slides.html` file

### 2. Audit the Code Block
In the `slides.html` file, the code block should follow this pattern:

```html
<div class="code-block">
  <p class="code-label">path/to/file.py</p>
  <pre><code class="language-python">
# Python code here — NO manual <span> tags
</code></pre>
</div>
```

**Check for:**
- ✅ `<code>` tag has `class="language-python"`
- ✅ No `<span class="cm">` or other manual color wrappers
- ✅ Code is plain text; highlight.js will handle all coloring
- ✅ Proper indentation preserved

### 3. Fix: Add Language Class
If the `<code>` tag is missing the language class:
```html
<!-- BEFORE -->
<pre><code>
@dataclass
class Result:
    status: str
</code></pre>

<!-- AFTER -->
<pre><code class="language-python">
@dataclass
class Result:
    status: str
</code></pre>
```

### 4. Fix: Remove Manual Color Spans
If manual `<span class="cm">` tags exist, remove them:
```html
<!-- BEFORE -->
status: str  <span class="cm"># MATCHED | RESOLVED</span>

<!-- AFTER -->
status: str  # MATCHED | RESOLVED
```

Highlight.js will automatically color the comment green with the vscode-dark-modern theme.

### 5. Verify the Fix
After editing the `slides.html` file:

1. Run the build script for that deck:
   ```bash
   cd training-materials/staging
   python3 scripts/build_deck.py --deck lab4-deck  # or lab1, lab2, etc.
   ```

2. Confirm no manual spans survived anywhere in the deck:
   ```bash
   grep -c 'class="cm"' lab4-deck/index.html   # must print 0
   ```

3. Confirm every code block declares its language:
   ```bash
   grep -o '<code[^>]*>' lab4-deck/index.html   # every hit needs language-python
   ```

4. Hard-refresh the browser (Cmd+Shift+R or Ctrl+Shift+R)

5. Navigate to the fixed slide and verify:
   - No literal `<span ...>` text appears anywhere in the block
   - Keywords are cyan/blue: `if`, `elif`, `class`, `def`, `return`, `import`
   - Strings are orange/tan: `"text"`, `'text'`, f-strings
   - Comments are green and italic: `# comment`
   - Numbers are light green: `123`, `0.5`
   - Class/function names are teal: `ReconResult`, `append`

## Affected Files
- `training-materials/staging/lab1-deck/sections/*/slides.html`
- `training-materials/staging/lab2-deck/sections/*/slides.html`
- `training-materials/staging/lab3-deck/sections/*/slides.html`
- `training-materials/staging/lab4-deck/sections/*/slides.html`
- `training-materials/staging/lab5-deck/sections/*/slides.html`
- `training-materials/staging/lab6-deck/sections/*/slides.html`
- `training-materials/staging/lab7-deck/sections/*/slides.html`
- `training-materials/staging/lab8-deck/sections/*/slides.html` (if exists)

## Theme Reference
The syntax highlighting uses `vscode-dark-modern.css` from highlight.js:
- **Keywords**: `#569cd6` (blue)
- **Strings**: `#ce9178` (coral/orange)
- **Comments**: `#6a9955` (green, italic)
- **Numbers**: `#b5cea8` (light green)
- **Built-ins/Classes**: `#4ec9b0` (teal)
- **Functions**: `#dcdcaa` (yellow)

## Quick Checklist
- [ ] Code block has `class="language-python"` on the `<code>` tag
- [ ] No manual `<span class="cm">` or other color spans remain
- [ ] `grep -c 'class="cm"' <deck>/index.html` returns 0
- [ ] Indentation is correct and preserved
- [ ] Syntax is valid Python
- [ ] Build script run: `python3 scripts/build_deck.py --deck [lab-name]`
- [ ] Browser cache cleared (hard refresh)
- [ ] No literal `<span ...>` text visible on the rendered slide
- [ ] All syntax elements display with expected colors
