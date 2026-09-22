# Reveal.js Animations — Fragment & Transition Rules

**Purpose:** describe how to add bullet-by-bullet reveal, entrance effects, and slide
transitions inside the deck's `slides.html` fragment files. Never edit generated
`index.html` files directly — rebuild with `python3 staging/scripts/build_deck.py`.

---

## Core concept: fragments

A **fragment** is any element that Reveal.js hides until the presenter advances (spacebar /
right arrow). Fragments are triggered in DOM order within a slide.

Add `class="fragment"` to the element you want to animate:

```html
<li class="fragment">This bullet appears on click</li>
```

Multiple fragments on one slide each require a separate advance. The slide does not move
forward until all fragments have been revealed.

---

## Fragment animation styles

Append a style class alongside `fragment` to change the entrance effect:

| Class | Effect |
|---|---|
| `fragment` (no extra class) | fade-in (default) |
| `fragment fade-up` | fade + slide up from below |
| `fragment fade-down` | fade + slide down from above |
| `fragment fade-left` | fade + slide in from right |
| `fragment fade-right` | fade + slide in from left |
| `fragment fade-out` | visible at first, fades out on advance |
| `fragment highlight-current-blue` | highlights blue while current, then stays normal |
| `fragment highlight-red` | turns red on reveal |
| `fragment grow` | briefly scales up on reveal |
| `fragment shrink` | briefly scales down on reveal |
| `fragment semi-fade-out` | fades to ~50% opacity when next fragment advances |

Example — bullets entering from the left:

```html
<ul class="split-bullets">
  <li class="fragment fade-left">First point</li>
  <li class="fragment fade-left">Second point</li>
  <li class="fragment fade-left">Third point</li>
</ul>
```

---

## Controlling order with `data-fragment-index`

By default, fragments fire in DOM order. Override with `data-fragment-index` to control
the sequence or make multiple elements appear at the same time:

```html
<!-- Both bullets appear on the same advance -->
<li class="fragment" data-fragment-index="1">Left column point</li>
<li class="fragment" data-fragment-index="1">Right column point (same step)</li>
<li class="fragment" data-fragment-index="2">This appears next</li>
```

---

## Animating nested content

Fragments inside nested elements work the same way. A common pattern is a card with a
title that's visible immediately, and bullets that appear one at a time:

```html
<div class="split-card">
  <h3>The habit</h3>           <!-- visible immediately -->
  <ul class="split-bullets">
    <li class="fragment fade-up"><strong>Glob</strong> backlog/*.md to see what's there.</li>
    <li class="fragment fade-up"><strong>Grep</strong> for the ticket header pattern.</li>
    <li class="fragment fade-up"><strong>Read</strong> only the one ticket you need.</li>
  </ul>
</div>
```

---

## Slide transitions

Set the transition style on the `<section>` tag with `data-transition`:

```html
<section data-transition="slide">   <!-- content slides in from right -->
<section data-transition="fade">    <!-- cross-fade -->
<section data-transition="zoom">    <!-- zoom in -->
<section data-transition="convex">  <!-- convex flip -->
<section data-transition="concave"> <!-- concave flip -->
<section data-transition="none">    <!-- instant cut -->
```

Control in/out independently:

```html
<section data-transition="slide-in fade-out">
```

---

## Background transitions

```html
<section data-background-transition="zoom">
```

Valid values: `none`, `fade`, `slide`, `convex`, `concave`, `zoom`.

---

## Speaker notes

Speaker notes are **not** fragments — they are always hidden from the audience and shown
only in the presenter view (press `S` in Reveal.js to open the presenter console).

Add an `<aside class="notes">` anywhere inside `<section>`. Place it last by convention:

```html
<section>
  <div class="slide-card">
    <!-- slide content -->
  </div>
  <aside class="notes">
    Talking point for the presenter. This text never appears on the main display.
    Include context, timing cues, or the tagline that was removed from the slide body.
  </aside>
</section>
```

---

## What NOT to do

- **Do not** add `class="fragment"` to the `<section>` itself — fragments live inside sections.
- **Do not** nest `<section>` inside a fragment; Reveal.js does not support that.
- **Do not** use CSS `animation` or `transition` properties to replicate fragment behavior —
  they fire immediately on load and cannot be controlled by the presenter.
- **Do not** hand-edit any generated `index.html`; always edit `slides.html` and rebuild.

---

## Quick-start checklist

1. Open the relevant `sections/<slug>/slides.html`.
2. Add `class="fragment"` (plus an optional style class) to each `<li>`, `<p>`, or `<div>`
   you want to reveal one step at a time.
3. Use `data-fragment-index` if multiple elements should appear simultaneously.
4. Move any presenter context to `<aside class="notes">` at the bottom of the `<section>`.
5. Run `python3 staging/scripts/build_deck.py` to regenerate `index.html`.
6. Open the deck in a browser and press `S` to verify speaker notes appear in presenter view.
