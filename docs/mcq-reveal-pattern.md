# MCQ Knowledge-Check Reveal Pattern

How the "Knowledge Check" slides animate options in one at a time and only
highlight the correct answer once every option for that question has
appeared. Canonical/working reference: `lab1-deck`.

## HTML structure

Each question is a `.mcq-item` containing its question text, its options
(one marked `.mcq-option-correct`), and a trailing zero-height `.mcq-reveal`
span. All of these are Reveal.js fragments (`class="fragment"`) with
sequential `data-fragment-index` values, so they animate in this order:
item → option a → option b → option c → reveal span → (next item...).

```html
<div class="mcq-list">
  <div class="mcq-item fragment" data-fragment-index="1">
    <p class="mcq-question">1. Question text?</p>
    <p class="mcq-option fragment" data-fragment-index="2">(a) ...</p>
    <p class="mcq-option mcq-option-correct fragment" data-fragment-index="3">(b) ...</p>
    <p class="mcq-option fragment" data-fragment-index="4">(c) ...</p>
    <span class="mcq-reveal fragment" data-fragment-index="5"></span>
  </div>
  <!-- next .mcq-item continues the fragment-index count (6, 7, 8, ...) -->
</div>
```

Notes:
- The correct option does not have to be `(b)` — mix up its position per
  question so the pattern isn't memorizable.
- The `.mcq-reveal` span is always the LAST fragment inside its `.mcq-item`.
  It has no visible content; it only exists to give the CSS gate below
  something to key off of.
- Fragment indices are a single running count across the whole slide, not
  reset per question.

## CSS gate

```css
.mcq-option-correct {
  color: var(--muted);
}

.mcq-reveal {
  display: block;
  height: 0;
  overflow: hidden;
}

.mcq-item:has(.mcq-reveal.visible) .mcq-option-correct {
  color: var(--teal);
  font-weight: 700;
}
```

The correct option stays muted until Reveal.js adds the `visible` class to
that question's own `.mcq-reveal` span (i.e. after all of that question's
options have animated in). Only then does the `:has()` rule match and turn
the correct option teal/bold.

## The bug to avoid

The `:has()` selector must be scoped to the individual `.mcq-item`, not to
the whole `section` (slide):

```css
/* WRONG — matches the whole slide, so ANY question's reveal fragment
   lights up EVERY question's correct answer on that slide at once. */
.reveal .slides section:has(.mcq-reveal.visible) .mcq-option-correct { ... }

/* RIGHT — scoped per question. */
.reveal .slides section .mcq-item:has(.mcq-reveal.visible) .mcq-option-correct { ... }
```

With the section-scoped version, as soon as the first question on the slide
finishes revealing, its `.mcq-reveal.visible` satisfies the `:has()` check
for the entire `section`, so every other question's correct answer turns
teal immediately — even ones the presenter hasn't reached yet. Always scope
the selector to `.mcq-item`, and avoid `!important`/reset hacks layered on
top of a mis-scoped rule; fix the scope at the source instead.

## Where this lives

- Canonical example: `lab1-deck/styles.css` (`.mcq-item:has(...)` block) and
  `lab1-deck/sections/02-mindset-shift/slides.html`.
- Shared by import: `lab5-deck/styles.css` defines the Reveal-integration
  version of this rule; `lab6-deck/styles.css` imports it rather than
  redefining it.
