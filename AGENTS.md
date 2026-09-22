# AGENTS.md — Staging Environment Rules

This file is the canonical source of truth for any AI agent (Claude Code, GitHub Copilot,
Cursor, etc.) working inside `trainig-materials/staging/`. All top-level `CLAUDE.md` and
`copilot-instructions.md` files in this workspace delegate here.

---

## CRITICAL: Always rebuild after editing slides

**Every `index.html` in a deck directory is a generated build artifact. Never edit it directly.**

The source of truth for slide content is `sections/<slug>/slides.html`. After any edit to a
`slides.html` file, you MUST rebuild before the change is visible in the browser:

```bash
cd /path/to/trainig-materials/staging
python3 scripts/build_deck.py
```

To rebuild a single deck:
```bash
python3 scripts/build_deck.py --deck lab2-deck
```

If you skip the rebuild step, the rendered deck will not reflect your changes, and the user
will report that the change "didn't work."

---

## Project structure

```
staging/
  scripts/
    build_deck.py          ← the build script; always run after editing slides.html
  shared/
    base.css               ← universal rules, imported by every deck (labs 1-8)
    dark-theme.css         ← navy-card system, imported by labs 3-8 only (not 1-2)
  lab1-deck/
  lab2-deck/
    sections/
      01-backlog-and-skills/
        slides.html        ← EDIT THIS, not index.html
    styles.css             ← @import shared/base.css + deck-specific rules only
    index.html             ← GENERATED — do not hand-edit
  lab3-deck/ lab5-deck/ lab7-deck/
  .claude/
    skills/                ← per-task SKILL.md files for this environment
      deck-section-rules/  ← cadence and structure rules for slides
      reveal-animations/   ← fragment/transition/speaker-notes patterns
      deck-pdf-export/     ← how to export a deck to PDF
```

---

## Shared CSS architecture

Each deck's `styles.css` is no longer a fully independent copy. It starts with:

```css
@import url("../shared/base.css");
@import url("../shared/dark-theme.css");   /* labs 3-8 only, not labs 1-2 */
```

followed by *only* what's genuinely unique to that deck (unique component classes, or a
deliberately-per-deck override like `.split-card h3`, which drifted between decks with no
clear reconciliation and was left alone rather than force-unified).

- **`shared/base.css`** — rules verified identical (or explicitly reconciled) across all 8
  decks: `:root` variables, Reveal.js integration, the Read→Decide→Act→Observe orbit graphic,
  the Knowledge Check/MCQ block, `.objectives-list`/`.split-bullets`, the `.slide-card`
  liquid-glass container, etc.
- **`shared/dark-theme.css`** — the navy/translucent card system (`.category-card`,
  `.survey-box`, `h1` margins, etc.) used by the Reveal-dark generation (labs 3-8). Labs 1-2
  intentionally keep their own lighter card treatment and don't import this file.

**Before adding a new rule to a deck's own `styles.css`**, check whether the same selector
already exists in `shared/base.css` or `shared/dark-theme.css` — if so, edit it there instead
so all decks stay in sync. This structure exists because labs 1-5 drifted independently for a
long time (different font sizes for the same components, e.g. the MCQ block ranged from
0.85rem to 1.48rem across decks) before being consolidated.

---

## Reveal.js conventions

- Slides are written as flat lists of `<section>...</section>` blocks — no `<html>/<head>/<body>` wrapper.
- Speaker notes go in `<aside class="notes">` inside the `<section>`, placed last by convention.
- Animated bullets use `class="fragment"` on `<li>` or other child elements.
- See `.claude/skills/reveal-animations/SKILL.md` for the full animation reference.
- See `.claude/skills/deck-section-rules/SKILL.md` for slide cadence and structure rules.

---

## CSS sizing conventions (lab2-deck)

| Selector | Current size | Notes |
|---|---|---|
| `.split-card h3` | 1.35rem | card heading |
| `.split-bullets` | 1.30rem | bullet body text |
| `.objectives-list` | 1.50rem | learner objectives list |

---

## Skills in this environment

Load a skill with `read_file` on the SKILL.md path before executing the workflow it describes.

| Skill | Path | Use when |
|---|---|---|
| `deck-section-rules` | `.claude/skills/deck-section-rules/SKILL.md` | creating or restructuring slides |
| `reveal-animations` | `.claude/skills/reveal-animations/SKILL.md` | adding fragment animations, transitions, speaker notes |
| `deck-pdf-export` | `.claude/skills/deck-pdf-export/SKILL.md` | exporting a deck to PDF |

---

## What NOT to do

- **Do not** edit any `index.html` by hand — the build script will warn and refuse to overwrite if you do.
- **Do not** add content to generated files — it will be lost on the next rebuild.
- **Do not** skip the rebuild and assume a `slides.html` edit is visible in the browser.
- **Do not** create new top-level deck `index.html` files manually — let `build_deck.py` generate them.
