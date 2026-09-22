---
name: nested-slide-cards
description: Build nested card grids within deck slides — layout templates and styling patterns
---

# Nested Slide Cards: Build Pattern & Markup

Use this skill whenever you're adding multiple concept cards, comparison boxes, or grid-based content within a training deck slide.

## The pattern

A **nested card grid** breaks complex concepts into bite-sized visual units, each with a title (h4) and one-line explanation. The cards sit inside a `.slide-card`, styled white with dark text for legibility and contrast.

## Grid layouts (choose one per slide)

### Two-wide grid (most common for comparisons)
```html
<div class="category-grid grid-two-wide">
  <div class="category-card">
    <h4>Concept A</h4>
    <p>One sentence explaining the concept, max two lines.</p>
  </div>
  <div class="category-card">
    <h4>Concept B</h4>
    <p>Parallel structure — same length, same tone as card A.</p>
  </div>
</div>
```

**Use when:** comparing two approaches (e.g., Autocomplete vs. Agentic Coding), showing before/after, or contrasting two phases of a workflow.

### Three-wide grid
```html
<div class="category-grid grid-three-wide">
  <div class="category-card">
    <h4>Phase 1</h4>
    <p>First step in sequence.</p>
  </div>
  <div class="category-card">
    <h4>Phase 2</h4>
    <p>Second step in sequence.</p>
  </div>
  <div class="category-card">
    <h4>Phase 3</h4>
    <p>Third step in sequence.</p>
  </div>
</div>
```

**Use when:** breaking a workflow into three discrete steps, or showing three equal-weight concepts.

### Five-wide grid (dense, for ingredient lists or capability breakdowns)
```html
<div class="category-grid grid-five-wide">
  <div class="category-card">
    <h4>Ingredient 1</h4>
    <p>Brief definition.</p>
  </div>
  <!-- Repeat 4 more -->
</div>
```

**Use when:** listing five distinct items (e.g., the Five-Ingredient Frame: Outcome, Scope, Verification, Deliverable, Guardrails) where each needs equal visual weight but minimal space.

## Card content guidelines

**Title (h4):** 2–4 words, noun-forward. Not a full sentence.
- ✓ "Copilot (Autocomplete)"
- ✓ "CLAUDE.md"
- ✗ "What is a CLAUDE.md file?"

**Body (p):** one sentence, max two lines at normal deck size. Same length across sibling cards in the same grid — visual consistency.
- ✓ "Multi-file refactorings, multi-repo work. You delegate an outcome and review the result — the agent owns the approach."
- ✗ "A long, rambling explanation of what this concept means and how it applies in real-world scenarios with many examples."

## Styling notes

Cards auto-style with:
- **Background:** white (#ffffff)
- **Text:** dark navy (#070c33 for h4, #3a3a3a for p)
- **Border:** subtle dark (rgba(0, 0, 0, 0.12))
- **Shadow:** soft drop shadow for depth

No additional classes needed — `.category-card` handles all styling.

## Context inside deck slides

Nested cards typically appear:

1. **After an eyebrow label** (e.g., `<div class="eyebrow">09:30 – 11:00 · The Agentic Mindset Shift</div>`)
2. **After the h1 slide title**
3. **Before longer-form content** (e.g., a detailed diagram, video placeholder, or agenda-style list)

This markup goes inside a section's `slides.html` fragment (e.g.
`day1-deck/sections/02-mindset-shift/slides.html`) as one Reveal `<section>...</section>` block,
wrapped in the standard `.slide-card` panel — never edit a generated `index.html` directly, edit
the fragment and re-run `python3 staging/scripts/build_deck.py`.

Example structure:
```html
<section>
  <div class="slide-card">
    <div class="eyebrow">Time range · Section name</div>
    <h1>Main idea</h1>

    <div class="category-grid grid-two-wide">
      <!-- Nested cards here: quick concept bites -->
    </div>

    <!-- Optionally: longer content below (diagram, list, box) -->
    <div class="mindset-shift">
      <!-- More detail -->
    </div>
  </div>
</section>
```

## Checking your work

- [ ] All cards in the same grid have titles and bodies (no empty cards)
- [ ] Titles are 2–4 words each, phrased as nouns
- [ ] Bodies are one sentence each, roughly equal length
- [ ] Grid choice matches the concept count (2-wide for pairs, 5-wide for ingredients, etc.)
- [ ] Grid is placed after the h1 title and eyebrow, before other content
- [ ] Cards read white-on-navy-navy (auto-applied; no custom bg/text classes needed)
