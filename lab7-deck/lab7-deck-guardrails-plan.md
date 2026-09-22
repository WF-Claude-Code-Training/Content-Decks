# Lab 7 deck rebuild plan — "Guardrails in an Agent Pod"

**Status: plan only. No deck files touched yet.** This is the iteration surface — we refine this
document, then implement against it (same workflow we used for the Lab 5 rebuild).

**Sources of truth for everything below:**
- [`Daily-Labs/lab-7-skills-subagents-hooks-coordination/README.md`](../../../Daily-Labs/lab-7-skills-subagents-hooks-coordination/README.md)
- [`Daily-Labs/lab-7-skills-subagents-hooks-coordination/ROLES.md`](../../../Daily-Labs/lab-7-skills-subagents-hooks-coordination/ROLES.md)
- [`Daily-Labs/DAY2-CHANGES.md`](../../../Daily-Labs/DAY2-CHANGES.md) (the "why we changed it" record)
- Current deck: [`sections/01-structured-logging-rollout/slides.html`](sections/01-structured-logging-rollout/slides.html)
- Prior (superseded) plan: [`lab7-deck-rebuild-plan.md`](lab7-deck-rebuild-plan.md)

---

## Top finding: the deck teaches the vehicle, not the lesson

The current `lab7-deck` (16 slides) is titled **"Add Structured Logging"** and organizes itself
around the logging *feature*: WM-109, the logging interface, threading it through three modules,
and the mechanics of *delegating a review* to a subagent. Hooks arrive late (slides 11–12) as one
technique among several.

Per `DAY2-CHANGES.md`, Lab 7's actual job is the **enforcement layer** — the three-layer control
model (Skill → subagent → hook) and, above all, *deciding which layer a guardrail belongs in* and
*managing those guardrails across a pod*. The README says it outright: "the important part is not
*how* to write a hook. It's learning which guardrails deserve one."

So this is the same reframe we did for Lab 5: **the feature is the vehicle, the framework is the
lesson.** Structured logging is to Lab 7 what `statement_delta` was to Lab 5 — the thing you build
*through*, not the thing the deck teaches. Slides should teach guardrails as a transferable
discipline; the WM-109 specifics belong on the handoff slide.

### What changes, in one table

| Dimension | Deck teaches now | Deck should teach |
|---|---|---|
| Framing | "Add structured logging" | "Build and manage the enforcement layer for a pod" |
| Spine | Skill delegates review to a subagent | Three layers of control, and choosing the right one |
| Hooks | A late technique (2 slides) | The center of gravity: what a hook is, the two shapes, the interface, when *not* to use one |
| Reviewers | One reviewer, delegated cleanly | **Two** reviewers that disagree, and adjudicating the collision |
| Pod management | Not covered | Session vs. agent-scoped hooks; contract-only vs. tool-enforced |
| Lab specifics | On content slides (logging interface, threading) | Demoted to the handoff slide |

> **Note:** the current deck's subagent-delegation slides (isolation, "what makes delegation
> safe", "reviewing a cross-cutting change") are solid teaching but belong to Lab 5's territory
> now. Keep the *two-reviewers-disagree* idea; fold or cut the rest so hooks and layer-choice get
> the room.

---

## The spine of the new deck: choosing the layer is the design work

Three ideas thread the whole deck and should be visible on the objectives slide, the framework
slide, and the recap:

1. **Three layers of control, and each fails differently.** A Skill fails *silently* (nobody
   invokes it). A subagent fails *arguably* (a reviewer can be wrong or talked around). A hook
   fails *loudly, or not at all* (it can't be reasoned with — that's the point).
2. **A hook is the only guardrail that isn't a request.** A Skill can be skipped, a reviewer
   talked around. A `PreToolUse` denial happens before the tool runs and doesn't negotiate. That's
   why it's reserved for mistakes you can't take back — and why hooking everything is its own
   mistake.
3. **Managing guardrails is a pod-level decision.** Where a guardrail lives (session-wide vs.
   attached to one role), and whether it's *enforced* or merely *contracted*, is the difference
   between a framework and a wish. This is where Lab 4's "contract-only" gap finally closes.

---

## Proposed slide progression

Target **~17 slides** — deliberately lean. Marked **NEW**, **REWRITE**, **KEEP-ish**, or **CUT**.

| # | Slide | Disposition | Purpose |
|---|---|---|---|
| 1 | **Title** — "Lab 7: Build the Enforcement Layer" | REWRITE | New title/subtitle; frame as guardrails, not logging |
| 2 | **Where Lab 7 Fits** (recap Lab 4/5 → this lab) | REWRITE | Labs 4/5 got work done *through* roles; this lab is the layer underneath |
| 3 | **Learning Objectives** | REWRITE | Full rewrite — see objectives below |
| 4 | **Three Layers of Control** (Skill / subagent / hook, + how each fails) | NEW | The spine. The table from `ROLES.md`: artifact, what it is, how it fails |
| 5 | **Choosing the Layer Is the Design Work** | NEW | The decision test; under-enforce vs. over-enforce cost |
| 6 | **A Hook Is the Only Guardrail That Isn't a Request** | NEW | Why enforcement is categorically different from a request |
| 7 | **Two Shapes of Hook: Additive vs. Subtractive** | NEW | General principle: "adds something forbidden?" vs. "removes something required?"; most real guardrails are subtractive |
| 8 | **The Hook Interface** (stdin JSON, exit 0/2, stderr is a prompt) | NEW (from old 11) | General mechanics, reusable for any `PreToolUse` hook |
| 9 | **Fail Open or Fail Closed?** | NEW | An explicit decision, made and written down; state the limitation (regex vs. AST) rather than discover it |
| 10 | **Read One, Write One** | NEW (from old 12) | The worked-example/authored pattern: additive example → subtractive one you write |
| 11 | **Watch It Deny You** | NEW | The round trip (request → deterministic refusal → reason). A hook that never denied you is one you don't trust |
| 12 | **Managing Guardrails in a Pod** (session vs. agent-scoped) | NEW | Where a hook lives; contract-only vs. tool-enforced; closes Lab 4's gap for real |
| 13 | **Two Reviewers Earn Their Keep by Disagreeing** | KEEP-ish (from old 8) | Conformance vs. audit sufficiency; adjudicating the collision is the deliverable |
| 14 | **What Not to Hook** | NEW | PII, scope-widening: a framework is defined by what it declines to enforce |
| 15 | **Lab 7 Handoff** (run sheet) | REWRITE (from old 13) | **Where the WM-109 specifics live**: the logging rollout, `audit_query`, the two hooks, `risk-officer` |
| 16 | **Knowledge Check** (MCQ) | REWRITE (from old 14) | Re-map to the new objectives — see MCQ section |
| 17 | **Recap: You Can Now...** | REWRITE (from old 15) | Restate objectives as accomplishments; the three-layer table as the takeaway |

### What to CUT or fold
- **Old slides 5–7** (three ways to reach a subagent / isolation decision test / what makes
  delegation safe) — strong content, but it's Lab 5's subagent-mechanics territory now. Cut, or
  compress the single most Lab-7-relevant point (subagents can't ask mid-task, so delegation is
  only *safe* when the brief is unambiguous) into a one-line footnote on slide 13.
- **Old slide 9** ("the delegation written into the Skill itself") — a nice detail, but it's about
  Skill phase flow, not guardrails. Cut, or fold one line into the handoff slide.
- **Old slide 10** ("the interface you'll thread through three modules") — pure feature mechanics.
  Move to the handoff slide.
- **Old debrief slide** ("add the logger, don't change the decision") — feature-specific. Fold its
  principle ("logging only; don't change behavior") into a guardrails callout on slide 15.

---

## Learner objectives — full rewrite

The current objectives are logging-rollout-shaped. Replace with the guardrail framework (5, lean):

1. **Place a guardrail in the right layer** — Skill (convention), subagent (judgment), or hook
   (unrecoverable) — using an explicit decision test, and explain how each layer fails.
2. **Distinguish the two shapes of hook** — additive ("adds something forbidden?") from
   subtractive ("removes something required?") — and recognize that most guardrails worth having
   are the harder, subtractive kind.
3. **Read a `PreToolUse` hook's contract** — stdin JSON, exit 0/2, stderr as a prompt to the model
   — and make the fail-open vs. fail-closed decision deliberately, writing down what the check
   can't catch.
4. **Manage guardrails across a pod**, choosing between a session-wide hook and one scoped to a
   single role, and explain how that closes the contract-only gap a `tools:` list leaves open.
5. **Adjudicate two reviewers that disagree** — conformance vs. audit sufficiency — by deciding
   and recording the outcome, never by loosening a checklist until it agrees.

> Objectives 1 and 5 are the two most load-bearing ideas: *choosing the layer* and *adjudicating a
> disagreement*. Keep them prominent.

---

## Best practices to surface as content (lean, generalized)

- **Choosing the layer is the design work.** Convention → Skill. Judgment → subagent.
  Unrecoverable → hook. Wrong in either direction has a cost: under-enforce and you rely on
  diligence; over-enforce and people route around the framework.
- **A hook is the only guardrail that isn't a request.** Reserve it for guardrails where a
  well-meaning mistake is unrecoverable.
- **Most real guardrails are subtractive.** "Did this remove something required?" needs the
  *simulated result* of the change vs. what's on disk — not just the text being introduced.
- **stderr is a prompt, not a log line.** A denial should name the legitimate alternative, not
  just refuse. Claude Code feeds it back to the model.
- **Make the fail-open/fail-closed call explicitly, and write down the limitation.** A hook with a
  known, documented blind spot is stronger than one with an assumed-perfect reputation.
- **Two reviewers earn their keep by disagreeing.** Conformance and sufficiency are different
  questions; one reviewer optimizing for both quietly favors whichever is easier to check.
- **A framework is defined as much by what it declines to enforce as by what it blocks.** "We
  considered a hook here and chose not to" beats never having thought about it.

## Risks / things to look for — surface as content, not just facilitator notes

- **The round trip is the proof.** A hook that passes tests but has never denied you anything is a
  hook you don't yet trust. Watch it deny a real edit and read the reason. (Slide 11.)
- **Weakening a hook to get past a denial is the failure mode.** "I needed a quick print to debug"
  is how guardrails get removed in real codebases. Sit with the friction once. (Slides 6, 11.)
- **A tools list gates tool *types*, not file *paths*.** "Edit, but only `test_*.py`" is
  unexpressable as a `tools:` list — which is exactly the gap an agent-scoped hook closes.
  (Slide 12.)
- **Resolving a reviewer disagreement by loosening a checklist destroys the point.** Adjudicate
  and record; don't pick a favorite. (Slide 13.)
- **Over-hooking trains people to ignore denials.** A PII check that fires on every string field
  is a nuisance, not a control. (Slide 14.)

## Payoffs — the "why this matters" beats to close on

- Lab 4 posed the question ("please don't touch that" is only a request); Lab 7 answers it (a hook
  makes it true).
- The enforcement layer is what turns a set of roles into a framework.
- Choosing *not* to enforce something is a design decision you can defend in a review.
- A guardrail you can't take back protects against a mistake you can't take back — and nothing
  else should get that treatment.

---

## `deck.json` metadata updates

- `title`: `"Lab 7: Build the Enforcement Layer"` (drop "Add Structured Logging")
- `subtitle`: keep `"Claude Code Developer Enablement"`
- `summary`: replace the logging-rollout summary with the guardrail framing — hold all three
  layers of control at once (Skill, subagent, hook), and decide which layer each guardrail belongs
  in.
- `sections[0].slug`: `01-structured-logging-rollout` → `01-enforcement-layer` *(optional; the
  slug is cosmetic. If renamed, rename the section directory in the same pass or the build breaks.)*
- `sections[0].title`: `"Structured Logging Rollout"` → `"Build the Enforcement Layer"`
- Block name / time: current deck says `13:30 – 14:45`. Confirm against the live agenda before
  changing.

## MCQ re-map (one per objective)

1. **A guardrail: "don't alter the fee-tier table during a logging rollout." Which layer?** → Hook.
   One careless edit misprices every fee, review already missed it once, and there's no legitimate
   exception during this work.
2. **What makes a hook "subtractive," and why is it harder than an additive one?** → It asks
   whether a change *removes* something required, so it must simulate the file after the edit and
   compare to disk — reading the tool input alone can't answer it.
3. **A `PreToolUse` hook exits 2 and writes to stderr. What happens to that message?** → Claude
   Code feeds it back to the model as a prompt to work around, so the denial should name the
   legitimate alternative, not just refuse.
4. **Why can't a `tools:` list express "this role may edit source but never tests"?** → A tools
   list gates tool *types*, not file *paths*; an agent-scoped `PreToolUse` hook is the missing
   expression that makes the rule tool-enforced.
5. **`logging-reviewer` approves; `risk-officer` flags a missing field. How do you resolve it?** →
   Decide and record — extend the convention or accept the gap in writing — never loosen a
   checklist until it agrees.

---

## Build / regeneration reminders (for implementation, later)

- Edit `sections/<slug>/slides.html` — **not** the generated `index.html`.
- After content edits: `python3 scripts/build_deck.py --deck lab7-deck` from `training-materials/staging/`.
- If `deck.json`'s `summary`/`title` change, also run a full `python3 scripts/build_deck.py` so the
  landing-page tile regenerates.
- If the section slug is renamed, rename `sections/01-structured-logging-rollout/` to match in the
  same pass, or the build won't find it.
- The turquoise picker marker is opt-in: put `data-nav-objectives` on the recap card's
  `slide-card` div so the recap gets the objectives color alongside the objectives slide (same fix
  applied to Lab 5).

## Open questions to resolve before implementing

1. **Slide budget.** 17 is lean already. If tighter, merge slides 8–9 (interface + fail-open) into
   one "hook mechanics" slide, or fold slide 11 (watch it deny you) into the handoff.
2. **How much logging feature survives on-slide?** Proposal: none as a teaching topic; WM-109, the
   logger interface, and `audit_query` appear only on the handoff slide as the applied vehicle.
   Confirm that's the right call, or keep one grounding slide.
3. **Agent-scoped hooks (slide 12)** are a stretch goal in the lab, not required. Decide whether to
   teach it as the headline of the pod-management slide or as a "here's how far it goes" footnote.
4. **Section slug rename** — cosmetic but touches the directory. Worth doing for consistency with
   the retitled deck, or leave as-is to avoid churn?
5. **Lab 4/5 recap accuracy** — source the recap from the current lab READMEs, not the older decks,
   since those were stale before their own rebuilds.
