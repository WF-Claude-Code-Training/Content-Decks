# Lab 5 deck rebuild plan — "Pod Ships a Feature"

**Status: plan only. No deck files touched yet.** This is the iteration surface — we refine this
document, then implement against it.

**Sources of truth for everything below:**
- [`Daily-Labs/lab-5-pod-ships-feature/README.md`](../../../Daily-Labs/lab-5-pod-ships-feature/README.md)
- [`Daily-Labs/lab-5-pod-ships-feature/ROLES.md`](../../../Daily-Labs/lab-5-pod-ships-feature/ROLES.md)
- [`Daily-Labs/DAY2-CHANGES.md`](../../../Daily-Labs/DAY2-CHANGES.md) (the "why we changed it" record)
- Current deck: [`sections/01-map-before-you-touch/slides.html`](sections/01-map-before-you-touch/slides.html)
- Prior (now-superseded) plan: [`lab5-deck-rebuild-plan.md`](lab5-deck-rebuild-plan.md)

---

## Top finding: the deck teaches a lab that has been superseded twice

The current `lab5-deck` (18 slides, section `01-map-before-you-touch`) covers **WM-114 only** as a
solo exercise: author one personal subagent (`change-impact-mapper`), confirm it delegates, map a
function's callers, ship `impact_note.md`. That was itself a rebuild of an even older
orchestration lab.

Per `DAY2-CHANGES.md`, Lab 5 has been rescoped again — and much bigger this time. It is now
**"Investigate, Migrate, Extend, Document: Ship a Feature Through the Pod."** The single-subagent
framing is now just *one part* (Part 3) of a four-part feature lifecycle run through a **five-role
pod**, across **two tickets**.

This is a full content swap, not an incremental edit. Recommend renaming the section slug
`01-map-before-you-touch` → `01-pod-ships-feature` and updating `deck.json` accordingly, rather
than patching slides in place.

### What actually changed, in one table

| Dimension | Deck teaches now (old) | Lab teaches now (new) |
|---|---|---|
| Framing | "Map before you touch" | "Ship a feature's full lifecycle through a pod" |
| Roles | 1 authored (`change-impact-mapper`, personal) | 5 total: 2 authored (`impact-mapper` personal, `release-scribe` project) + 3 carried forward from Lab 4 (`implementer`, `test-author`, `contract-reviewer`) |
| Tickets | WM-114 only | WM-114 (investigate + migrate) **and** WM-118 (extend + document) |
| Code written | None (a note only) | A six-file migration **and** a brand-new function (`statement_delta`) with no pre-written test suite |
| The headline lesson | Transitive impact | The **hand-off** — a feature moving between roles across its lifecycle |
| Verifiable targets | `check_impact_note.py` | 4 targets: `test_backdated_statements.py`, `check_statement_delta.py`, `check_impact_note.py`, `check_pod.py` |
| Recap of Lab 4 | `strategy-reviewer` (a role that no longer exists) | The three-role pod: `implementer` / `test-author` / `contract-reviewer` |

> **Stale cross-reference to fix while we're here:** the current deck's recap slide refers to Lab
> 4's `strategy-reviewer`. That role was **deleted** in the Day-2 revision (see `DAY2-CHANGES.md`
> §1). Lab 4 now ships `implementer`, `test-author`, and `contract-reviewer`. Every callback to
> Lab 4 in this deck must be re-sourced.

---

## The spine of the new deck: the hand-off is the product

The single most important reframe. The old deck's climax was *transitive impact* (what a `grep`
can't find). That lesson survives — but it's demoted to the migration half. The **new** climax is
the **feature lifecycle hand-off**: one ticket moving through five roles, where the interesting
moments are the *seams* between roles, not any single role's output.

Three ideas thread the whole deck and should be visible on the objectives slide, the pattern
slide, and the recap:

1. **The Read → Decide → Act → Observe loop doesn't change — it composes.** Lab 5 runs it twice,
   once per ticket: WM-114's Read is mapping a blast radius, WM-118's Read is reframing a vague
   ticket. Same loop, different phase content, not a new mnemonic for Day 2.
2. **Deciding a role *doesn't* apply is the same skill as deciding it does.** `impact-mapper` does
   real work on WM-114 and *nothing* on WM-118 — on purpose, because WM-118 changes no signatures.
   A pod that reaches for every role on every ticket has learned nothing.
3. **Personal vs. project scope is a distribution decision, made concrete by friction.** Two roles
   are authored; three must be *physically copied* from Lab 4 because they're project-scoped. The
   copy step is the lesson — `impact-mapper` (personal) needs no copy; the three project roles do.

---

## Proposed slide progression

Target ~18–20 slides (roughly the current length; the lab is bigger but slides should stay dense,
not multiply). Marked **NEW**, **REWRITE**, **KEEP-ish**, or **CUT**.

| # | Slide | Disposition | Purpose |
|---|---|---|---|
| 1 | **Title** — "Lab 5: Ship a Feature Through the Pod" | REWRITE | New title/subtitle, both tickets on the badge (WM-114 + WM-118) |
| 2 | **Where Lab 5 Fits** (recap Lab 4 → this lab → Lab 6) | REWRITE | Re-source Lab 4 recap to the three-role pod; frame this lab as the lifecycle escalation |
| 3 | **Learning Objectives** | REWRITE | Full rewrite — see objectives section below |
| 4 | **The Same Loop, Twice** (Read→Decide→Act→Observe, once per ticket) | REWRITE (keeps R→D→A→O, redefines it) | Shows the loop composing across WM-114 and WM-118 rather than introducing a new mnemonic |
| 5 | **Deciding What Belongs in the Pod** | NEW (implemented) | General framework for adding a role: one job per role, separation of concerns, isolate verbose work, least privilege by design, complexity only when it earns its place. Cites Anthropic's *Building Effective Agents* |
| 6 | **Where Multi-Agent Breaks Down** | NEW (implemented) | The counterweight, anchored on the Anthropic *Multi-Agent Research System* quote on parallelizable vs. dependency-heavy work. Ties straight to WM-118 skipping `impact-mapper` and to serializing edits |
| 7 | **Meet the Pod** — five roles, who owns what across the two tickets | NEW (implemented) | The role×ticket matrix from `ROLES.md`; introduce tool-enforced vs contract-only |
| 8 | **Two Authored, Three Carried Forward** | NEW (implemented) | The scope/distribution lesson made concrete via the `cp` friction |
| 9 | **Personal vs. Project Scope: a Distribution Decision** | REWRITE (from slide 10) | Same core content, but anchored to `impact-mapper` (copy-free) vs the three copied roles |
| 10 | **Anatomy of a Subagent** (name/description/tools/model) | KEEP-ish | Still valid; add least-privilege framing for the two *new* roles' tool budgets |
| 11 | **Ticket 1 — WM-114: Investigate + Migrate** | REWRITE (from slide 8) | Ground the migration half; six files, two that never mention pricing |
| 12 | **Investigate: Map Before You Touch** (direct/transitive/not-reached) | KEEP-ish (from slide 12/17) | Transitive impact lesson — now explicitly framed as *one phase*, not the whole lab |
| 13 | **Migrate Safely: Order, Semantics, What Must Not Change** | NEW | The three migration decisions; dependency-order editing; the back-compat trap |
| 14 | **The Silent Failure: Over-Migration** | NEW | `target_weights` — the parameter that shouldn't be added; why a reviewer needs a criterion for it |
| 15 | **Two Jobs, One Role: Repair vs. Originate** | NEW (merges old 13+14) | General principle: a test-authoring role either repairs a test a change made stale, or originates tests from raw criteria before code exists — and neither job ever belongs to the role writing the implementation, because a red test gives an implementer two ways to go green and only one is legitimate |
| 16 | **A Verifier Is a Floor, Not the Spec** | REWRITE (generalized) | Any automated checker — a test suite, a linter, `check_pod.py`, a hand-written script — proves a minimum bar, not completeness; naming what your own judgment covers beyond it is part of the deliverable, for *any* checker, not one ticket's |
| 17 | **Confirm Delegation + Measure Context** | REWRITE (merge slides 7/11/12) | Proactive vs explicit; the orchestrator-worker isolation payoff, measured via `/context` |
| 18 | **Shared Working Tree: Fan Out Reads, Serialize Edits** | REWRITE (generalized) | General property of subagents (and any concurrent editors): one working tree, not private clones. Read/review work parallelizes free; anything holding `Edit`/`Write` doesn't — concurrent edits silently overwrite each other with no error |
| 19 | **Lab 5 Handoff** (the six parts, as a run sheet) | REWRITE (from slide 14) — **also where slides 15–18's principles get grounded**: WM-118 as the no-pre-written-spec ticket, `check_statement_delta.py` as this lab's floor-not-spec instance, the six-file migration as this lab's shared-working-tree instance | Orient → Staff → Investigate → Migrate → Extend → Deliver |
| 20 | **Knowledge Check** (MCQ) | REWRITE | Re-map questions to the new objectives — see MCQ section |
| 21 | **Recap: You Can Now...** + Debrief | REWRITE (merge 16/17/18) | Restate objectives as accomplishments; the role×ticket matrix as the debrief artifact |

> **Why the merge and generalization:** slides 15–19 previously taught `statement_delta`,
> `check_statement_delta.py`, and "six files" directly — content that only serves one run of one
> lab. The deck's job is to teach the transferable principle; the lab is where it gets applied.
> Pushing the concrete nouns (WM-118, the six files, the specific checker) down into the Handoff
> slide keeps slides 13–16 reusable even if this lab's tickets change again, the way Lab 4's
> `strategy-reviewer` reference just went stale under the old deck.

**Net change vs. current deck:** the single "author one subagent and prove it delegates" arc
(slides 6–13) contracts to ~3 slides (5–7 + 15), freeing room for the migration half (9–12) and
the generalized test-origination/verification/shared-working-tree half (13–14, 16), which the
current deck has *nothing* on — all three now framed as transferable principles rather than one
ticket's specifics, with the concrete WM-118 application living on the Handoff slide instead.

### What to CUT outright
- Nothing about the R→D→A→O slide itself — **keep the loop**, just redefine it (see new slide 4).
  The prior plan's recommendation to drop the loop assumed a flat four-phase arc; running it twice,
  once per ticket, avoids that problem without abandoning the course's one recurring throughline.
- The **standalone "Code Example: the prompt" slide** (current slide 13) as a *dedicated* slide.
  There are now multiple briefs (mapper, migration, test-author). Fold one representative brief
  into the relevant content slide rather than spotlighting the mapper prompt alone.

---

## Learner objectives — full rewrite

The current five objectives are all about authoring *one* subagent and measuring context. They
undersell the lab now. Proposed replacement set (5–6, one per major teaching beat):

1. **Run the Read → Decide → Act → Observe loop twice on one feature** — once for WM-114
   (investigate + migrate), once for WM-118 (extend + document) — using a pod of five roles, and
   explain why each pass hands off to a different role.
2. **Staff a pod across repositories**, distinguishing roles you *author* (personal scope, no copy
   needed) from roles you must *carry forward* (project scope, physically copied), and justify each
   role's scope as a distribution decision rather than a capability one.
3. **Map a change's blast radius before editing** — naming direct callers, transitive callers, and
   the function a change provably does *not* reach — and recognize that a map stopping at direct
   callers is wrong, not merely incomplete.
4. **Migrate existing code safely across multiple files** in dependency order, preserving exact
   behavior for every current caller, and detect **over-migration** — a signature changed that
   didn't need to change — as a silent failure with no error message.
5. **Originate tests from a ticket before any implementation exists** (`test-author`'s first job),
   reframing an underspecified ticket first, and treat a checker as a *floor* by naming explicitly
   what your tests cover that it does not.
6. **Decide when a role does *not* apply** to a ticket, and defend that omission as a deliberate
   choice — the same judgment as deciding a role *does* apply.

> Objective 4's "over-migration" beat and objective 6's "role doesn't apply" beat are the two ideas
> most unique to this rebuild; keep them prominent rather than folding them into others.

---

## Best practices to surface as content (explicit stakeholder ask)

Work these into content slides, not footnotes:

- **The hand-off is the work.** The seam where a red test becomes a *different role's* job is the
  lesson. Most failures in this lab are hand-off failures, not coding failures.
- **Fan out reads; serialize edits.** One shared working tree, not private clones per role. Reads
  and reviews parallelize for free; concurrent edits silently overwrite each other with no error.
  Taught generally on slide 16; grounded in this lab's six-file migration on the Handoff slide.
- **Least privilege by tool budget.** `impact-mapper`: `Read, Grep, Glob` only (it runs *before*
  any edit — a mapper that can edit has skipped the decision it exists to inform). `release-scribe`:
  `Read, Write`, explicitly **no** `Edit` (keeps a doc pass from becoming a code pass).
- **A vague `description` is the #1 reason proactive delegation silently fails** — carry this
  forward from the old deck; it's still true and still worth naming.
- **Context isolation is the mechanism, not a side effect** — the orchestrator-worker pattern
  (Anthropic's multi-agent-systems writeup). The subagent reasons in its own window; only its
  summary re-enters the main conversation. Lab 5 is where you *measure* it (`/context` before/after).
- **A note that lists files is a diff; a note that tells the advisor team whether their integration
  breaks is a release note.** Write the second one. (`release-scribe`'s judgment line.)

## Risks / things to look for — surface as content, not just facilitator notes

- **Over-migration has no error message.** `target_weights` will pass every test if you thread
  `as_of_date` through it — and it should never have gotten the parameter. Only an explicit reviewer
  criterion catches it. (Slide 12.)
- **The back-compat trap.** `as_of_date` defaults to `None`, never to "today" — a default that
  *computes* today looks identical until the day the history and the price table disagree. (Slide 11.)
- **`compute_trades` reaches pricing twice** (directly + via `current_weights`). Forward the date to
  only one call site and trades land on the right symbol, right direction, wrong dollar amount.
  Exactly one test catches it; a human reviewer likely wouldn't. (Slide 11.)
- **Writing the tests yourself defeats the point of splitting the role.** If you (or `implementer`)
  write `statement_delta`'s tests because it's faster, the general lesson from slide 13 — test
  origination is never the implementer's job — slipped past you on the one ticket built to teach it.
- **Passing the floor isn't done.** `check_statement_delta.py` skips a real case on purpose (a trade
  whose amount changed but symbol/action didn't). Say what your tests add on top — the concrete
  instance of slide 14's general "a verifier is a floor" principle.

## Payoffs — the "why this matters" beats to close on

- A feature has a lifecycle, not just a diff — and the pod owns the whole thing.
- Independence is what you're buying, not speed: a reviewer with no memory of writing the code and
  no ability to change it catches a class of bug no self-review ever will.
- Configuration/scope is a governance decision — who owns a role, who reviews it, who inherits its
  cost — not a refactor.
- The system got *faster to correct*, not *better at guessing* — same escalate-don't-guess principle
  as Day 1, now with a data-owned reference table behind it.

---

## `deck.json` metadata updates

- `title`: `"Lab 5: Ship a Feature Through the Pod"` (drop "Map Before You Touch")
- `subtitle`: e.g. `"Investigate, migrate, extend, and document a real feature through a five-role pod."`
- `summary`: replace the single-subagent summary with the lifecycle framing — a full feature run
  through the pod across two tickets, WM-114 and WM-118.
- `sections[0].slug`: `01-map-before-you-touch` → `01-pod-ships-feature`
- `sections[0].title`: `"Map Before You Touch"` → `"Ship a Feature Through the Pod"`
- Ticket badge (title slide): `WM-114` → `WM-114 + WM-118`
- Block name / time: confirm against the current agenda before changing (the old plan moved this to
  11:00–12:30; the lab is now longer — README budgets ~105–120 min. Verify the live block.)

## MCQ re-map (one per objective)

1. **Why must `impact-mapper` be copied nowhere, while `implementer` must be physically copied into
   this repo?** → `impact-mapper` is personal-scoped (already on your machine, every repo);
   `implementer` is project-scoped and doesn't follow you across repos on its own.
2. **On WM-118, `impact-mapper` does no work. Why is that correct rather than an oversight?** →
   WM-118 adds a new function and changes no existing signature, so there's no blast radius to map.
3. **What is "over-migration," and why does no test catch it by default?** → Adding a parameter to a
   function that didn't need it (`target_weights`); every behavioral test still passes, so only an
   explicit reviewer criterion flags it.
4. **Why must `test-author` write `statement_delta`'s tests before `implementer` writes the code,
   and not from `check_statement_delta.py`?** → It's the one ticket with no pre-written spec;
   originating tests from criteria is `test-author`'s actual first job, and the checker is a floor,
   not the spec.
5. **A change-impact map lists only the three direct callers of `get_price`. Why is that map wrong,
   not just incomplete?** → It misses transitive callers (`check_drift`, `build_statement`) that a
   migration planned off it would wrongly call safe.

Keep the transitive-impact debrief table and the "answer key" (`DIRECT_CALLERS` /
`TRANSITIVE_CALLERS`) slide from the current deck — they're still accurate and land the migration
half well. Just reframe their headers so they read as *one phase* of the lab, not its conclusion.

---

## Build / regeneration reminders (for implementation, later)

- Edit `sections/<slug>/slides.html` — **not** the generated `index.html`.
- After content edits: `python3 scripts/build_deck.py --deck lab5-deck` from `training-materials/staging/`.
- If `deck.json`'s `summary`/`title` change, also run a full `python3 scripts/build_deck.py` so the
  landing-page tile regenerates.
- Rename the section directory (`sections/01-map-before-you-touch/` → `sections/01-pod-ships-feature/`)
  in the same pass as the `deck.json` slug change, or the build won't find it.

## Open questions to resolve before implementing

1. **Slide budget.** 19 slides is still a lot for one block. If the live block is tight, which half
   compresses — merge slides 11–12 (migrate + over-migration), or fold slide 14 (verifier-is-a-floor)
   into slide 13 (repair vs. originate) as one general-principles slide?
1a. **Should slides 9–12 get the same generalization treatment as 13–16?** They currently teach
    WM-114 via its own specifics (`target_weights`, the six named files) rather than the general
    principles underneath (over-migration as a category of silent failure; migration ordering by
    dependency graph, not by file count). Out of scope for this pass since it wasn't asked for, but
    flagging the same inconsistency exists there and would benefit from the identical treatment.
2. **Does the deck show `release-scribe` at all, or is it mentioned only in passing?** It does real
   work (writes `impact_note.md`) but is conceptually light. Proposed: one card on slide 5, no
   dedicated slide.
3. **Lab 4 recap accuracy** depends on Lab 4's own deck being rebuilt (it's also stale per the prior
   plan). Source the recap from `lab-4-subagent-pod-intro/README.md` directly, not `lab4-deck`.
4. **Context-measurement beat** — keep as its own emphasis (old slide 12) or fold into slide 16?
   It's a strong stakeholder-requested moment; recommend keeping it visible on slide 16.
