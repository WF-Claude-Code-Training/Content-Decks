# Deck Section Structure & Format Rules

**Purpose:** standardize how learning decks are organized across the 3-day program. Each
section follows a consistent rhythm: learner objectives up front (what you'll be able to do),
content and interaction, a knowledge check MCQ, then objectives restated at close to close the
loop and ensure retention.

**Where slides live:** decks are Reveal.js presentations generated from per-section fragment
files, not hand-written HTML pages. Each section is a folder under `<day>-deck/sections/<slug>/`
containing a single hand-edited `slides.html` (a flat list of Reveal `<section>...</section>`
blocks — no `<html>/<head>/<body>` wrapper). Add or edit slides there, then regenerate every
`index.html` in the deck with `python3 staging/scripts/build_deck.py` — never hand-edit a
generated `index.html` directly (the script's content-hash guard will refuse to overwrite it and
warn you if you do). See `nested-slide-cards.md` for the card/grid markup patterns to use inside
a fragment, and `day1-deck/sections/02-mindset-shift/slides.html` as a worked example of the full
cadence below (Mindset Shift → Five-Ingredient Frame → Loop → CLAUDE.md/Skills → Responsible AI
→ Benchmark → MCQ → Objectives Restated).

---

## The cadence: Objectives → Content → MCQ → Objectives Restated

Every section (morning, afternoon, lab framing, recap) follows this shape.

**Exception — purely administrative/logistics sections** (environment setup, survey slides,
agenda overview): keep the Objectives slide if there's a real self-check goal (e.g., "verify
your environment works"), but skip the MCQ — there's no teaching content yet to test. Don't
force a knowledge check where nothing was taught.

### 1. **Opening slide: Learner Objectives** (1–2 slides)
- **Placement:** at the start of every section.
- **Content:** 3–5 crisp, observable outcomes phrased as "by the end you can..." or "you will be
  able to..."
- **Sourcing:** draw from the agenda HTML's section objectives (green `<li>` under
  `<div class="objectives">`) or the relevant lab's README "Lab outcomes" section.
- **Tone:** specific enough that a learner can self-assess ("Can I name three when to use Plan
  mode?" — yes/no — rather than "Understand Plan mode" — mushy).
- **Never:** don't mix this with content. The learner needs to know what success looks like
  before the section starts.

### 2. **Content section** (slides and lab time)
- **Placement:** immediately following the objectives.
- **Content:** the section's lecture, demo, discussion, or hands-on lab. Use the agenda's
  "Detail & Outcomes" column and each lab's README to structure this.
- **Pacing:** can be multiple slides + hands-on time. The important constraint is that
  learners see the objectives first, *then* content unfolds toward those targets.
- **Order matches the objectives list, in order.** If objective 1 is "describe loop X" and
  objective 2 is "package X into artifact Y," the slide that teaches X comes before the slide
  that teaches Y — don't teach a downstream mechanism before the concept it depends on just
  because it was easier to build first. If a later concept is a genuine prerequisite for an
  earlier objective's content (e.g. objective 1 is the loop, but the loop's *deep* explanation
  needs vocabulary from objective 2's content), split the difference: teach a plain version of
  the earlier objective's concept first (no borrowed vocabulary), then circle back for a deeper
  pass once the prerequisite has been introduced — don't reorder the objectives themselves to
  make the slide order easier.

### 3. **Knowledge check: MCQ** (1 slide)
- **Placement:** right before the wrap-up.
- **Format:** 3–4 multiple-choice questions (one correct answer, plausible distractors).
- **Sourcing:** write questions that directly map to the opening objectives — if the
  objective says "name a task where Plan mode beats default mode," the MCQ should ask
  exactly that.
- **Scoring:** optional in live delivery (can be a verbal show-of-hands), but the slide shows
  the right answer so learners can self-check.
- **Tone:** not a gotcha quiz. The questions are straightforward checks on the core ideas,
  so a learner paying attention in the content section can answer them.

#### MCQ animation pattern (preferred)

Each question card animates in as a unit, options appear one at a time, then the correct
answer highlights in teal — no separate "Answer: (b)..." line needed.

**HTML structure per question:**
```html
<div class="mcq-item fragment" data-fragment-index="N">
  <p class="mcq-question">Question text</p>
  <p class="mcq-option fragment" data-fragment-index="N+1">(a) wrong answer</p>
  <p class="mcq-option mcq-option-correct fragment" data-fragment-index="N+2">(b) correct answer</p>
  <p class="mcq-option fragment" data-fragment-index="N+3">(c) wrong answer</p>
  <span class="mcq-reveal fragment" data-fragment-index="N+4"></span>
</div>
```

- The container (`mcq-item`) fades in with the question text on step N.
- Options (a), (b), (c) each appear on their own advance (N+1, N+2, N+3), all in muted color.
- The `<span class="mcq-reveal">` is invisible (no content, no height). When it becomes
  `.visible` on step N+4, the CSS rule below fires and turns the correct option teal —
  no extra text, no separate answer line.

**Required CSS (already in `lab2-deck/styles.css`):**
```css
.mcq-option {
  font-size: 1.35rem;
  color: var(--muted);
}

.mcq-item:has(.mcq-reveal.visible) .mcq-option-correct {
  color: var(--teal);
  font-weight: 700;
}
```

The `:has()` selector watches each card independently — revealing Q1's answer does not
affect Q2's card. Use sequential `data-fragment-index` values across all questions (e.g.
Q1 uses 1–5, Q2 uses 6–10, etc.) so the presenter advances through them in order.

### 4. **Closing slide(s): Objectives Restated** (1 slide)
- **Placement:** last slide(s) of the section (before the next section starts or before
  break/lunch).
- **Content:** repeat the opening objectives *verbatim* (same list).
- **Purpose:** explicit closure. The learner sees "here's what you came to learn" at the top,
  and "here are those same things — did you get them?" at the close. The repetition is the
  learning tool.
- **Optional add:** for multi-day material (especially Day 2–3), add a thin callback: "You
  can do this now. Watch for these skills again on [Day N]."

---

## Example: how to apply this to a section

**Section: "Plan Mode & Test-Driven Delivery" (agenda block at 15:30–16:30, Day 1)**

Agenda objectives (from Claude-Training-3-Day-Agenda.html):
- Give Claude a verifiable target (a spec or failing test) and use plan mode to approve the
  plan before it executes.

Lab objectives (from labs/lab3/README.md):
- Understand that failing tests *are* the verifiable target.
- Use Plan mode to propose changes before executing.
- Implement test-driven (TDD) — failing test first, then code.
- Recognize when a verified acceptance criterion improves execution.

**Opening slide: Learner Objectives**
```
By the end of this block, you can:

1. Explain what Plan mode does and when to reach for it instead of default mode.
2. Use a failing test as the "spec" before writing code (test-driven delivery).
3. Describe the analyze → plan → implement → verify → deliver flow.
4. Recognize when a verified acceptance criterion improves both the plan and the implementation.
```

**Content** (20m lecture + 10m demo + 30m lab, per agenda)
- Why one-shot execution isn't enough for high-stakes changes.
- The five-ingredient frame + failing test = verifiable target.
- Live demo: enable Plan mode, show Claude proposing a plan, human approving it.
- Lab 3: WM-110 drift alert false positives (failing test → plan → implement).

**Knowledge check MCQ**
```
Which scenario is a good fit for Plan mode?
a) Adding a print statement to a logging function you've never seen before.
b) Fixing a fee calculation where a failing test already defines the acceptance criteria.
c) Renaming a variable in a single line.
d) Doing a dry-run of a CLI tool.

[Correct answer: b]
```

**Closing slide: Objectives Restated**
```
By the end of this block, you can:

1. Explain what Plan mode does and when to reach for it instead of default mode.
2. Use a failing test as the "spec" before writing code (test-driven delivery).
3. Describe the analyze → plan → implement → verify → deliver flow.
4. Recognize when a verified acceptance criterion improves both the plan and the implementation.

✓ You've done this live in Lab 3. Watch for these skills again in Day 2 (Lab 7's
  deterministic checks) and Day 3 (Strangler Fig refactoring).
```

---

## Notes for deck authors

### Sourcing objectives
- **Agenda source (primary):** `staging/schedule-doc/Claude-Training-3-Day-Agenda.html` has an
  `<ol>` of "By the end of this section you can..." under each section. Use those as the spine.
- **Lab source (secondary):** each lab's README has a "Lab outcomes" section. Use those to
  deepen and make lab-specific what the agenda says. For example, the agenda says "Recognize
  when iterative, stateful tool use outperforms one-shot prompting"; Lab 4's README says "build
  an agent loop" and "resolve what known strategies explain, escalate what they don't." The lab
  outcomes are more concrete — use those in the opening slide.

### MCQ sourcing
- **From the objectives:** write a question for each objective (or group a couple if they're
  tightly related).
- **Distractor quality:** distractors should be things a learner *might* think if they misheard
  the content, not obviously wrong. Example: if the objective is "know when to use Plan mode,"
  don't offer "Plan mode is for breakfast" as a distractor — offer "Plan mode is only for
  machine learning tasks" (plausibly sounds right if you weren't fully attending).
- **Answer key:** always show the right answer after the quiz section moves on, so learners
  can self-check without waiting for a facilitator.

### Rhythm and retention
- The opening objectives set an **intent contract** with the learner: "here's the deal for the
  next 90 minutes."
- The content **fulfills the contract** by teaching toward those specific outcomes.
- The MCQ **verifies the contract** — learner confirms they can do what they said they'd learn.
- The objectives restatement **closes the loop** — explicit confirmation, plus a forward callback
  to later material if relevant.

This pattern works because it's *predictable* — learners know what to expect and can pace
their attention accordingly. Vary the content freely, but keep the frame consistent.

---

## Checklist for deck sections

- [ ] Opening objectives slide pulls from agenda HTML (primary) + lab README (secondary)
- [ ] Objectives are phrased as observable outcomes ("can name X," "can implement Y") not vague
      descriptors
- [ ] Content section exists with lecture/demo/lab pacing clear
- [ ] MCQ has 3–4 questions, each aligned to one objective
- [ ] MCQ distractors are plausible (not obviously wrong)
- [ ] Closing slide restates objectives *verbatim*
- [ ] If Day 2+, closing slide has a callback to future sections/labs
- [ ] Section flows: Objectives → Content → MCQ → Objectives Restated (each as its own Reveal `<section>` in the fragment, clear slide boundaries)
