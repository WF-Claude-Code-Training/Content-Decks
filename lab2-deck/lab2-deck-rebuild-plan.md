# Lab 2 deck rebuild — teaching points to add

**For a separate run.** This is a plan, not an implementation — no section slides have been
touched (only the top-level landing-page tile in `deck.json` was already corrected). Source of
truth for all content below: [`lab2-standalone/README.md`](../../../claude-labs-ttt/lab2-standalone/README.md),
[`AGENTS.md`](../../../claude-labs-ttt/lab2-standalone/AGENTS.md),
[`labs/lab2/fee_rollout.py`](../../../claude-labs-ttt/lab2-standalone/labs/lab2/fee_rollout.py),
[`.claude/skills/scoped-bugfix-flow/SKILL.md`](../../../claude-labs-ttt/lab2-standalone/.claude/skills/scoped-bugfix-flow/SKILL.md),
and the current [`Claude-Training-3-Day-Agenda.html`](../schedule-doc/Claude-Training-3-Day-Agenda.html)
(Day 1, 13:30–14:45 block).

## Top finding: `lab2-deck` is built around a task that isn't the current Lab 2

`training-materials/staging/lab2-deck/sections/01-backlog-and-skills/slides.html` teaches
**"Backlog Audit + Your First Team Skill"** — Glob/Grep/Read navigation of `backlog/`, a
three-lane "Manual vs Dump vs Glob+Grep" cost-race game built on `labs/lab2/audit.py`, and
authoring a Skill to ship an extension to `frame audit`, verified by `test_audit.py`. None of
that is the current Lab 2. The current Lab 2 (Day 1, 13:30–14:45, "Claude Code Interface & Team
Skills" / agenda title **"Reusable Skills for Fee Calculations"**) is a **two-pass fee-logic
rollout**: Pass 1 uses the existing generic `scoped-bugfix-flow` Skill to fix
`quarterly_advisory_fee`'s cliff-rate bug; Pass 2 has the learner author their own
fee-specific Skill to fix the *same* bug in the analogous `monthly_advisory_fee`, verified by
`test_fee_rollout.py`. The backlog-audit exercise still exists in `lab2-standalone/` but is
explicitly **optional and secondary** — the README calls it out under "Optional context
exercise (not primary)" and says to "treat it as triage signal only, not a second
implementation project." Building the entire deck's core narrative around it inverts the
lab's own priority.

This is the same shape of finding as the Lab 4/5/7/8 rebuilds — the ticket/task changed under
the deck — but with an important difference: **most of this deck's Skill-authoring pedagogy is
still valid and reusable**, because `scoped-bugfix-flow` is the same Skill in both the old and
current lab, and the generic mechanics of a `SKILL.md` (frontmatter anatomy, "USE WHEN"
auto-discovery vs. explicit `/<skill-name>` invocation, TodoWrite making phases visible,
checking for an Anthropic-hosted Skill before authoring one) don't depend on which ticket
they're taught against. **This rebuild is a re-grounding, not a full rewrite** — swap the
concrete task/code/tests everywhere they appear, keep the Skill-anatomy teaching slides,
restructure around the two-pass shape the current lab actually has.

Recommend: keep the section slug `01-backlog-and-skills` as-is (renaming it is optional and
lower-value here, since the section covers Skills broadly, not just backlog audit) — the
learner-facing fixes matter more than the folder name. If renaming, `01-fee-skill-rollout`
would better match the new content.

**Already fixed in this pass:** `deck.json`'s top-level `title` ("Lab 2 — Fee Logic Rollout with
Two-Pass Skills") and `summary` now describe the current lab accurately, so the root landing
page tile is no longer misleading — but the deck's own slides still teach the old task until
this plan is implemented.

## What carries forward unchanged (don't rebuild these)

- **"Anatomy of a SKILL.md"** (name / description+USE WHEN / ordered workflow steps) — still
  exactly how `scoped-bugfix-flow` and any learner-authored Skill are structured. No change
  needed beyond checking the slide doesn't reference `frame audit`-specific examples.
- **"Anthropic-Hosted Skills You Can Download"** — a general point about checking
  `github.com/anthropics/skills` before authoring from scratch. Unchanged.
- **"Two Ways In: Auto-Discovery and `/<skill-name>`"** — still accurate; the slash-command
  parallel to `/model` is generic. Unchanged.
- **"Watch Your Skill Run" (TodoWrite)** — the point that a skipped/out-of-scope phase is
  feedback on the Skill's wording is generic. Only the example task named in the bench-note
  ("invoke your Skill on a real task frame — e.g. a `--top N` flag for `frame audit`") needs to
  change to the monthly-fee task.
- **The Lab 1 → Lab 2 recap framing** ("Lab 1: you consumed one, Lab 2: you author one," both
  naming `scoped-bugfix-flow`) — already accurate for the current lab, since `scoped-bugfix-flow`
  really is the Pass 1 Skill. No change needed.

## What must change

1. **The core task, everywhere it's named.** `labs/lab2/audit.py` / `frame audit` /
   `test_audit.py` / backlog tickets → `labs/lab2/fee_rollout.py` /
   `quarterly_advisory_fee` / `monthly_advisory_fee` / `test_fee_rollout.py`. This touches the
   grounding slide, the "Read Stage" slides, the race-game slide, the "Watch Your Skill Run"
   bench-note, and the MCQ.
2. **The lab's actual two-pass shape isn't represented at all currently.** The deck has no
   "Pass 1 / Pass 2" slide — it jumps straight to "author your own Skill." Add a slide that
   makes the two passes explicit: Pass 1 (use the existing generic Skill, unmodified, on
   `quarterly_advisory_fee`) establishes the baseline pattern; Pass 2 (author a fee-specific
   Skill, on the analogous `monthly_advisory_fee`) is where the domain-specific value gets
   added. This is the lab's actual teaching point — **do the same fix twice, once generic and
   once specialized, to feel the difference** — and it's currently missing entirely.
3. **What a fee-specific Skill adds beyond the generic one.** The README is explicit:
   progressive marginal tiers only (no cliff-rate), exact breakpoint correctness, monotonic
   non-decreasing fee for increasing AUM, preserve public method signatures, run targeted +
   full tests. Worth a slide naming these five as the domain rules a generic bugfix flow
   wouldn't know to check — this is the "why a specialized Skill, not just the generic one
   again" argument, and the deck currently has no equivalent.
4. **The Read stage's `/context` and `/usage` slides use backlog-audit examples** in their
   "reusable kickoff" prompts (e.g. "Use `/context` with WM-102 ticket + `labs/lab2/audit.py`").
   Reword the example to the fee module (e.g. "Use `/context` with `WM-202-fee-rollout.md` +
   `labs/lab2/fee_rollout.py`, then summarize the cliff-rate bug"). The underlying point
   (`/context` scopes the read, `/usage` makes cost visible) is unchanged.
5. **The race game (Manual vs Dump vs Glob+Grep) is hard-coded to `audit.py`.** Either retire
   it (since the backlog audit it demonstrates is now the *optional* exercise, not the graded
   task) or reframe it explicitly as "the optional context exercise" and keep it as a clearly
   secondary/time-permitting slide rather than the deck's centerpiece interactive moment. Given
   the standalone README's own framing ("triage signal only, not a second implementation
   project"), recommend demoting it to an optional closing slide, not building the main flow
   around it.
6. **The `test_audit.py` reference in the MCQ (Q4)** needs to become `test_fee_rollout.py`, and
   the question should ask about the verification target for the *fee-specific Skill's* fix
   (monthly), not a generic "your own Skill" extension.

## Objectives slide — suggested rewrite

Replace the current backlog/Glob-Grep-centric objectives with something like:
- Use an existing generic Skill (`scoped-bugfix-flow`) to fix a scoped, verifiable bug —
  progressive-tier fee logic for `quarterly_advisory_fee` — without needing to look inside it.
- Author your own Skill (`.claude/skills/<your-name>-fee-standardization-flow/SKILL.md`) that
  encodes domain rules a generic flow wouldn't know, and apply it to the analogous
  `monthly_advisory_fee` bug.
- Identify what a fee-specific Skill adds beyond the generic one: progressive marginal tiers,
  exact breakpoint correctness, monotonic fee behavior, and signature preservation.
- Distinguish Claude's built-in capabilities, Anthropic's downloadable Skills, and the Skill you
  author yourself — and recognize which to reach for.
- (Optional, time-permitting) Use Glob/Grep/Read to triage `backlog/` and contrast that against
  dumping every file into context — a secondary exercise, not the graded deliverable.

## Metadata updates needed in `deck.json`

Already done in this pass:
- `title`: "Lab 2 — Fee Logic Rollout with Two-Pass Skills" ✅
- `summary`: rewritten to describe the two-pass quarterly/monthly fee rollout ✅

Still to confirm/update when the slides are rebuilt:
- The section's own eyebrow/title-slide text (`13:30 – 15:15 · Backlog Audit + Your First Team
  Skill`) should become `13:30 – 14:45 · Reusable Skills for Fee Calculations` — the agenda's
  current time for this slot is 13:30–14:45, not 13:30–15:15.
- `meta-row` on the title slide: `Ticket` → `WM-202` (currently likely absent or referencing the
  wrong ticket — confirm against the live title slide when editing).

## Recap slide ("Where Lab 2 Fits") — update inputs/outputs

- **Recap · Lab 1** should stay grounded in WM-101 (management-fee tiered-breakpoint fix via a
  starter Skill) — this part is likely already accurate; confirm against `lab1-deck`.
- **This lab** bullets need to change from "navigate backlog, author a Skill for `frame audit`"
  to "use the existing Skill on quarterly, author your own on monthly — same bug, twice, to
  feel when a domain Skill earns its keep."
- **Next** bullet pointing at Lab 3 (Plan Mode & TDD, WM-110 drift alert) is likely already
  accurate — confirm against `lab3-deck`, no change expected.

## Code examples to source

- `labs/lab2/fee_rollout.py` — `annual_progressive_fee` (used by quarterly) and the cliff-rate
  `_annual_cliff_rate` (used by monthly) — a good side-by-side "same bug, duplicated on
  purpose" code slide, mirroring the deck's existing code-example slide style.
- `.claude/skills/scoped-bugfix-flow/SKILL.md`'s phase flow (Analyze → Implement → Verify →
  Deliver) as the Pass 1 code example — this Skill already exists in the standalone package, no
  need to invent one.
- `test_fee_rollout.py`'s `-k quarterly` / `-k monthly` filtering as the verification-target
  example, replacing `test_audit.py`.

## MCQ sourcing (map one question per objective)

1. Why does Pass 1 use the *existing* generic Skill unmodified, rather than writing a new one
   right away? (→ to establish the baseline pattern and prove the generic flow works before
   deciding whether the second, analogous bug needs something more specialized.)
2. What does the fee-specific Skill from Pass 2 need to check that the generic
   `scoped-bugfix-flow` doesn't know to check on its own? (→ progressive marginal tiers, exact
   breakpoint correctness, monotonic fee behavior, preserved signatures — the domain rules.)
3. What must a Skill's frontmatter `description` include for Claude Code to reach for it on its
   own? (→ unchanged from the current deck — a "USE WHEN" trigger phrase.)
4. What's the verification target for the Pass 2 fix? (→ `pytest labs/lab2/test_fee_rollout.py
   -k monthly -v`, then the full file, then the full suite — not `test_audit.py`.)

## Out of scope for this pass, but worth a follow-up check

- **The backlog-audit race game's JS/HTML is a substantial, hand-built interactive widget**
  (timers, cost comparison, live winner calculation). If it's demoted to an optional slide
  rather than removed, it's worth deciding whether to keep it wired to `audit.py` (since that's
  what the optional exercise actually runs) rather than reskinning it to the fee module, which
  would misrepresent what command the optional exercise runs. Flagging the decision, not making
  it here.
- **`lab1-deck`'s and `lab3-deck`'s recap/next-up callbacks to Lab 2** should be spot-checked
  once this rebuild ships, the same way Lab 5/7/8's shipped decks needed a one-line check after
  each other rebuild. Not fixed here.
- The rebuild itself: after editing `sections/01-backlog-and-skills/slides.html`, run
  `python3 scripts/build_deck.py --deck lab2-deck` from `training-materials/staging/` — the
  root landing page's `deck.json`-derived tile is already correct and doesn't need a further
  full rebuild unless `summary` changes again.
