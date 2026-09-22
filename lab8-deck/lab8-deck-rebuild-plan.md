# Lab 8 deck rebuild — teaching points to add

**For a separate run.** This is a plan, not an implementation — no deck files have been
touched. Source of truth for all content below: [`lab8-standalone/README.md`](../../../claude-labs-ttt/lab8-standalone/README.md),
[`AGENTS.md`](../../../claude-labs-ttt/lab8-standalone/AGENTS.md),
[`.claude/agents/codebase-mapper.md`](../../../claude-labs-ttt/lab8-standalone/.claude/agents/codebase-mapper.md),
[`.claude/agents/pattern-scout.md`](../../../claude-labs-ttt/lab8-standalone/.claude/agents/pattern-scout.md),
[`templates/recommendation-one-pager.md`](../../../claude-labs-ttt/lab8-standalone/templates/recommendation-one-pager.md),
and — for grounding the recap slide accurately — [`lab7-standalone/README.md`](../../../claude-labs-ttt/lab7-standalone/README.md).

## Top finding: `lab8-deck` currently covers a lab that no longer exists at this slot

`training-materials/staging/lab8-deck/deck.json` and its one section
(`01-governed-cicd-release-gate`) describe **a governed CI/CD merge-request gate** — a
two-layer (structural + live-review) pipeline check defended against prompt injection,
`labs/lab8/pr_review.py` / `ci_review.py`. That content still exists in the repo's history but
no longer maps to Lab 8 — the current Lab 8 (Day 2, 15:00–16:30, "Capstone: Skill & Subagent
Recommendation") is **a synthesis capstone, not a new mechanic**: participants run two
pre-built subagents (`codebase-mapper`, `pattern-scout`) in parallel against a real codebase
(their own team's, or the course repo as a fallback), cross-reference the two independent
reports themselves, and produce a short citation-backed recommendation of which Skills and
Subagents are worth building there — verified by presenting it to the room, not by a test file.
This is the same shape of finding as the Lab 5 and Lab 7 rebuilds — a full content swap, not an
incremental addition — but the user's own framing for this pass is correctly lighter-weight:
**this lab introduces no new mechanic**, so the deck's job is mostly to introduce the lab and
set clear expectations for the one real deliverable (the presentation), not to teach five new
concepts.

Recommend: rename the section to something like `01-put-it-all-together` (update `deck.json`'s
`sections` entry and slug), rather than patching gate/injection-defense slides in place.

**Note on the orphaned content.** The governed-CI/CD gate material isn't being thrown away —
`labs/lab8/pr_review.py` / `ci_review.py` still exist and still work, they simply no longer map
to any lab slot in the current 8-lab progression. Worth a decision above this rebuild about
whether that content resurfaces elsewhere (Day 3's continuous-build material reuses some of
this governance language already) or is retired outright — flagging, not deciding, here.

## Why this deck should stay intentionally light

Every other rebuild so far (Lab 5, Lab 7) introduced a genuinely new mechanic — a personal
subagent authored from scratch, a Skill that delegates to a subagent internally. **Lab 8
introduces nothing new mechanically.** Both subagents are pre-built and handed to the learner;
running two subagents in parallel is already familiar from Lab 5's orchestration; the
Skill-vs-Subagent decision criteria are the same ones from Lab 4/5, just applied cold to real
code instead of a toy fixture. The one genuinely new thing is **the human synthesis step
itself** — cross-referencing two independent reports into a judgment call neither subagent made
— and **the verification mechanism** — a presentation that survives peer challenge, since
there's no test file for "was this a good recommendation." The deck should spend its slides on
those two things, not invent teaching points that aren't in the lab.

## New content this lab introduces (not covered by any earlier deck)

1. **Two subagents run in parallel, and neither depends on the other.** `codebase-mapper`
   (architecture, entry points, data flow, hotspots) and `pattern-scout` (repetition → Skill
   signals, risk → Subagent signals) are dispatched together, the same "no ordering dependency,
   so don't serialize it" instinct from Lab 5's orchestration — just with two named subagents
   instead of N identical ones.
2. **The synthesis is not delegated — that's the actual point.** Cross-referencing the two
   reports, and applying the Lab 4/5 Skill-vs-Subagent test to each overlap, is done by the
   human in the main conversation. A third subagent doesn't do this step; delegating the
   judgment call itself would defeat the lab's purpose.
3. **A presentation is a legitimate verifiable target.** Every earlier lab's Verification
   ingredient was something automated (a test file, a checker script, a gate). This lab's is a
   ~3-minute presentation that has to survive a peer challenge — worth naming explicitly as the
   honest substitute for open-ended, judgment-heavy work that doesn't reduce to a script.
4. **Read-only enforcement matters more here because the blast radius isn't controlled.**
   `pattern-scout`'s `Bash` tool is hook-restricted to read-only `git` history commands
   (`validate-readonly-git.sh`, a `PreToolUse` hook) — worth calling out that this is the first
   lab where the target might be a codebase the learner doesn't fully own yet (their team's, not
   a lab fixture), so the enforced restriction is protecting something real.
5. **Data governance is a named constraint, not a footnote.** The lab explicitly reuses Day 1's
   data-governance rule (only point these subagents at a codebase already inside Wells Fargo's
   approved Claude Code access path) and gives a fallback (the course repo itself, or
   `lab4-standalone`/`lab5-standalone`) if a participant's team codebase isn't accessible that
   way. Worth a one-line callout, not a full slide.

## Objectives slide — suggested rewrite

Replace the current gate/injection-defense objectives with something like:
- Run two independent, read-only subagents in parallel against a real codebase and read their
  reports before doing anything else.
- Cross-reference two subagents' independent findings into a citation-backed judgment call —
  the synthesis step neither subagent makes for you.
- Apply the Skill-vs-Subagent decision test from Lab 4/5 cold, to code you didn't grow in this
  course.
- Defend a written recommendation to peers, and treat a presentation that survives challenge as
  a legitimate verifiable target when no test file can substitute for judgment.

## Metadata updates needed in `deck.json`

- `title`: "Lab 8 — Put It All Together" (drop "Governed CI/CD: a PR Release Gate for Change
  Quality")
- `subtitle`: something like "Two subagents, run in parallel, synthesized by you — the
  Skill-vs-Subagent call, applied cold to real code"
- `summary`: replace the gate/injection-defense summary with the codebase-mapper/pattern-scout
  synthesis-and-recommendation summary
- Meta-row: this lab has no WM ticket (it targets whatever codebase the learner brings, not a
  fixed fixture) — replace the `Ticket` field with something like `Deliverable` →
  `my-recommendation.md`, rather than inventing a ticket number that doesn't exist in the
  standalone package.
- Block name: "Governed CI/CD, Injection Defense & Quality Gates" → "Capstone: Skill & Subagent
  Recommendation" (matches the current agenda's block title for this slot)
- Time: `15:30 – 17:30` → `15:00 – 16:30` (confirmed against the current
  `Claude-Training-3-Day-Agenda.html`)

**Flag — the shipped agenda's own prose for this slot is itself stale, do not source content
from it.** `Claude-Training-3-Day-Agenda.html` (line ~515) describes Lab 8 as "review the
Logging Skill they just built... recommend one additional Skill or subagent... written, not
presented, and used to populate the backlog" — this contradicts `lab8-standalone/README.md`,
which is explicit that the deliverable *is* presented (~3 minutes, Part 6, "Verified by a short
presentation, not a test file") and uses two named subagents the HTML text never mentions. The
working draft (`Claude-Training-3-Day-Agenda-PRODUCTIVITY-DRAFT.md`, line ~206) matches
`lab8-standalone` almost verbatim (`codebase-mapper` / `pattern-scout`, presented, 15:00–16:15)
— that draft is the accurate description, the shipped HTML's prose is the stale one, even
though the HTML file is dated one day *after* the draft. Use the **shipped HTML's time/block
label only** (15:00–16:30, "Capstone: Skill & Subagent Recommendation" — close enough to the
draft's 16:15 to not matter for a slide), and source every other line of content from
`lab8-standalone`, not from either agenda doc's prose. Worth flagging back to whoever owns the
agenda doc that the shipped HTML needs a prose correction independent of this deck rebuild.

## Recap slide ("Where Lab 8 Fits") — update inputs/outputs

- **Recap · Lab 7** needs to change from "PreToolUse/PostToolUse hooks that block protected-file
  edits and redact PII" to what Lab 7 *actually* currently teaches per
  `lab7-standalone/README.md`: a Skill (`structured-logging-rollout`) implements a shared
  logging abstraction across three modules, and the Skill's own Phase C delegates review to a
  subagent (`logging-reviewer`) — i.e., Lab 7 is where "a Skill can delegate to a subagent
  internally" first appears.
- **This lab** bullets need to change from "structural check + governed live review, fail-closed
  MR pipeline" to "two pre-built subagents in parallel, human synthesis, presented
  recommendation" — and should explicitly name this as the point where Labs 4, 5, and 7's
  separate lessons (a subagent you're handed / a subagent you author / a Skill that delegates)
  get applied together, cold, to a real codebase — which is the literal meaning of "put it all
  together."
- **Next** bullet should point at Day 3 as a new arc (legacy/modernization work), not claim this
  same gate "anchors the continuous build" — that claim belonged to the old CI/CD content and
  doesn't hold for the new one.

## The "Pattern" slide

This lab doesn't introduce a new runtime shape — it reuses "two independent calls, fanned out
in parallel" from Lab 5 and applies it to two *different, named* subagents instead of N
identical ones. Recommend a simple sequential-parts table like Lab 5's (Orient → Build was
Lab 5; here it's **Install → Orient → Fan-out → Synthesize → Present**), not a runtime
Read→Decide→Act→Observe loop — same reasoning as the Lab 5 plan's call on this point, and for
the same reason: this is lab **parts**, not a runtime loop over a batch.

## Code examples to source

- `codebase-mapper.md`'s frontmatter + its four-part report shape (Shape / Entry points / Data
  flow / Complexity hotspots) — a good "what a read-only mapper produces" slide.
- `pattern-scout.md`'s frontmatter, specifically its `hooks:` block wiring
  `validate-readonly-git.sh` to `PreToolUse` — the enforced-restriction example, and a callback
  to Lab 7's hooks material without re-teaching hooks from scratch.
- `templates/recommendation-one-pager.md`'s five sections as the deliverable shape — short
  enough to show in full on one slide.

## MCQ sourcing (map one question per objective)

1. Why run `codebase-mapper` and `pattern-scout` in parallel instead of one after the other?
   (→ neither depends on the other's output — sequencing them wastes the point of delegating,
   the same reasoning as Lab 5's fan-out.)
2. Who does the cross-referencing between the two subagents' reports? (→ the human, in the main
   conversation — that synthesis is deliberately not delegated to a third subagent.)
3. A hotspot `codebase-mapper` flags but `pattern-scout` doesn't — is it automatically a strong
   Skill/Subagent candidate? (→ no; overlap between the two reports is the stronger signal, and
   every candidate still has to pass the Lab 4/5 Skill-vs-Subagent test on its own merits.)
4. Why is a presentation an acceptable verifiable target here, when every earlier lab used a
   test file or checker script? (→ the deliverable is open-ended judgment about real, varied
   code — a defensible presentation that survives peer challenge is the honest substitute when
   no deterministic check can grade "was this a good recommendation.")

## Out of scope for this pass, but worth a follow-up check

- **`lab7-deck`'s own recap/next-up line currently name-drops the old Lab 8.** Its closing slide
  says "Watch for this same Skill + subagent composition again in Lab 8's governed CI/CD" — that
  claim no longer holds once this rebuild ships. Not fixed here (touches an already-shipped
  deck), but flagged as a near-certain one-line follow-up once Lab 8 ships: something like
  "Watch for this same Skill + subagent composition again in Lab 8's capstone."
- **The shipped agenda HTML's own Lab 8 prose is stale**, independent of anything this deck does
  (see the flag under "Metadata updates" above). Worth a short correction pass on
  `Claude-Training-3-Day-Agenda.html` itself so future rebuilds don't have to re-discover this
  same discrepancy. Not fixed here — that file is outside `staging/lab8-deck/` and touches a
  document other decks also read from.
- The rebuild itself: after editing `sections/01-.../slides.html`, run
  `python3 scripts/build_deck.py --deck lab8-deck` from `training-materials/staging/` (and a
  full `python3 scripts/build_deck.py` if `deck.json`'s `summary` changes, since the top-level
  landing page tile is generated from it too) — don't hand-edit the generated `index.html` files.
