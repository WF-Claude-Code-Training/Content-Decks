# Lab 5 deck rebuild — teaching points to add

**For a separate run.** This is a plan, not an implementation — no deck files have been
touched. Source of truth for all content below: [`lab5-standalone/README.md`](../../../claude-labs-ttt/lab5-standalone/README.md),
[`AGENTS.md`](../../../claude-labs-ttt/lab5-standalone/AGENTS.md),
[`check_impact_note.py`](../../../claude-labs-ttt/lab5-standalone/check_impact_note.py), the
current [`Claude-Training-3-Day-Agenda.html`](../schedule-doc/Claude-Training-3-Day-Agenda.html)
(Day 2, 11:00–12:30 block), and — for grounding the recap slide accurately —
[`lab4-standalone/README.md`](../../../claude-labs-ttt/lab4-standalone/README.md) and
[`.claude/agents/strategy-reviewer.md`](../../../claude-labs-ttt/lab4-standalone/.claude/agents/strategy-reviewer.md).

## Top finding: `lab5-deck` currently covers a lab that no longer exists at this slot

`training-materials/staging/lab5-deck/deck.json` and its one section
(`01-orchestration-and-model-right-sizing`) describe **WM-111 — Nightly Pricing Triage
Orchestrator**: fan out N subagents in parallel over failed batch jobs, right-size the model
per task (Haiku/Sonnet/Opus), warm a prefix cache, then run an eval harness to baseline and
improve a triage prompt. That code still exists and still works
(`claude-labs-ttt/labs/lab5/orchestrate.py`, `eval_harness.py`), but the current agenda no
longer places it at Lab 5 — the current Lab 5 (Day 2, 11:00–12:30, "Understanding Existing
Systems") is **WM-114 — Map Before You Touch**, a completely different lab: the learner
**authors their own personal-scoped subagent** to trace a function's direct and transitive
callers before a risky signature change, and confirms it gets **proactively delegated to**, not
just explicitly invoked. This is the same shape of finding as the Lab 7 rebuild — a full content
swap, not an incremental addition.

Recommend: rename the section to something like `01-map-before-you-touch` (update `deck.json`'s
`sections` entry and slug), rather than patching orchestration/eval-harness slides in place.

**Note on the orphaned content.** The orchestration/right-sizing/eval-harness material isn't
being thrown away by this rebuild — it simply no longer maps to any lab slot in the current
8-lab progression. `claude-labs-ttt/AGENTS.md` (repo root) still describes it as "Lab 5" too, so
this staleness isn't confined to the deck. Worth a decision above this rebuild about whether that
content resurfaces elsewhere (a later lab, a Day-3 appendix) or is retired outright — flagging,
not deciding, here.

## New teaching points this lab introduces (not covered by any earlier deck)

1. **The learner authors the subagent this time — Lab 4 handed them one pre-built.** Lab 4's
   `strategy-reviewer` shipped ready-made, project-scoped, in `.claude/agents/`. Lab 5 flips
   that: the learner writes `change-impact-mapper`'s frontmatter themselves (`name`,
   `description`, `tools`, `model`) and immediately discovers that the `description` field
   *is* the mechanism other things in this lab depend on — get it right, and Claude reaches for
   it unprompted; get it vague, and Claude just does the work inline instead. A "you configured
   it, so you own whether it works" framing is a genuinely new beat.

2. **Personal vs. project scope is a distribution decision, not a context-efficiency one —
   and that's a subtle, easy-to-get-wrong point worth its own slide.** Both scopes get the
   *same* isolated, fresh context window once the subagent is invoked — that part doesn't
   change. What changes is *who pays the always-loaded cost of the description* and *where the
   subagent travels*: a personal subagent (`~/.claude/agents/`) loads into every session on the
   engineer's machine from now on, in every repo; a project subagent (`.claude/agents/`, checked
   in) is scoped to, and shared by, one repo's team. The test the lab teaches: is this rule
   specific to *this codebase* (→ project, like Lab 4's reconciliation-strategy rubric), or a
   habit the engineer wants *everywhere* (→ personal, like tracing callers before a change)?

3. **Proactive (automatic) delegation vs. explicit invocation — and Lab 5 is the first lab
   that makes the learner observe both, not just trigger one.** Every subagent use up to this
   point (Lab 4's `strategy-reviewer`) was invoked by name, every time — "did it delegate" was
   never in question. Lab 5's Definition of Done requires *both*: at least one delegation Claude
   made on its own, matching the task against `change-impact-mapper`'s `description` with no
   explicit ask, and at least one explicit invocation as a controlled comparison. Worth a slide
   framing this as a two-path test: ask the same question once without naming the subagent, once
   with — and notice whether the first one actually delegated (if it didn't, that's a signal to
   rewrite the description, not a broken feature).

4. **Context-window savings become something you measure, not something you're told.**
   Every earlier lab that touched context isolation (Lab 4's `strategy-reviewer`) asserted the
   benefit. Lab 5's README makes it an actual optional exercise: check `/usage` (or the context
   indicator) before and after delegating, then compare that against asking Claude to read and
   grep all six files inline in the main conversation instead. This is the strongest, most
   concrete "context window savings" moment in the course so far and deserves a dedicated slide
   with the before/after framing made explicit, per the stakeholder ask that this messaging come
   through clearly.

5. **Transitive impact is the actual point of "map before you touch" — not direct callers.**
   A plain `grep get_price(` finds the three direct callers in one pass; anyone could do that
   without a subagent. The lesson is what a keyword search *can't* find: `build_statement` in
   `statements.py` never mentions pricing anywhere in its own body, yet it's fully exposed to
   the change because it depends on `advisory_fee`, `compute_trades`, and `check_drift`, all of
   which depend on `get_price` transitively. Naming the one function *not* affected (and why) is
   equally part of the deliverable — a note that only lists things that break isn't more useful
   than a note that lists everything.

6. **An operational gotcha worth a one-line callout, not a full slide.** A freshly created
   `~/.claude/agents/` directory isn't picked up until Claude Code restarts — a learner whose
   first personal subagent silently never gets used is not hitting a bug, they haven't restarted
   yet. Small, but worth putting in the handoff slide so it doesn't eat lab time as confusion.

## Industry best-practices & context-savings messaging (explicit ask — make sure this lands)

The stakeholder asked specifically that context-window-savings and industry-best-practice
framing for subagents come through clearly in this rebuild. Concretely, work these into the
content slides (not just a footnote):

- **Context isolation is the mechanism, not a side effect.** The subagent's own Read/Grep/Glob
  reasoning over all six files happens in its own window; only a short summary — direct callers,
  transitive callers, the one function not affected — crosses back into the main conversation.
  This is the same **orchestrator-worker** shape Anthropic's own multi-agent-systems engineering
  writeup describes (the main conversation as orchestrator, the subagent as an isolated worker),
  even without fan-out to multiple subagents — the isolation property is identical at n=1.
  **Lab 5, not Lab 4, is the more natural first place to name this term explicitly**, because
  it's the first lab where the learner *measures* the payoff via `/usage` rather than being told
  about it. (See the "out of scope" note below — this has a knock-on effect on how Lab 7's deck
  currently phrases its own callback to this idea.)
- **A well-written `description` field for automatic delegation is itself a best practice worth
  naming, not an implementation detail.** Write it the way you'd write a function name a router
  has to match against: specific and task-shaped ("finds every direct and transitive caller of a
  target function across the project"), not generic ("helps understand code"). A vague
  description is the single most common reason proactive delegation silently doesn't happen.
- **Least-privilege tool grants are a default posture, not a one-off choice.** `Read, Grep, Glob`
  only — the same enforced-read-only pattern from Lab 4's `strategy-reviewer`, reinforced here as
  a pattern that holds regardless of scope (personal or project) or job (review vs. exploration).
- **Verify delegation happened; don't assume it.** The Definition of Done says "observed, not
  assumed" for a reason — a good habit to name explicitly as a subagent best practice: check
  that the tool call actually fired (transcript/tool-use indicator), the same way Lab 4 taught
  checking a subagent's verdict rather than trusting a claim.

## Objectives slide — suggested rewrite

Replace the current orchestration/right-sizing/eval-harness objectives with something like:
- Author a personal-scoped subagent (`~/.claude/agents/`) with a `description` specific enough
  to be matched automatically against a task, not just invoked by name.
- Distinguish personal from project subagent scope as a question of distribution and ownership
  (who inherits the always-loaded cost, where it travels) — not a difference in runtime
  isolation, which is identical either way.
- Confirm and contrast proactive (automatic) delegation against explicit invocation for the same
  task, and explain what in the subagent's definition drives which one happens.
- Measure, not just assert, the context-window savings a subagent's isolated window buys you,
  by comparing delegated vs. inline exploration cost.
- Produce a change-impact note that names every direct *and transitive* caller of a target
  function — and the one function genuinely unaffected, and why.

## Metadata updates needed in `deck.json`

- `title`: "Lab 5 — Map Before You Touch" (drop "Multi-Agent Orchestration, Right-Sizing &
  Eval Harnesses")
- `subtitle`: something like "Author your own subagent, confirm it gets delegated to, and
  measure the context you save by isolating the search"
- `summary`: replace the orchestration/eval-harness summary with the WM-114 change-impact-mapping
  summary
- Ticket badge: `WM-111` → `WM-114`
- Block name: "Orchestration & Cost" → something like "Understanding Existing Systems" (matches
  the current agenda's block title for this slot)
- Time: `09:30 – 11:00` → `11:00 – 12:30` (the agenda has moved this lab — confirmed against the
  current `Claude-Training-3-Day-Agenda.html`, unlike Lab 7 where the old plan said "keep as-is
  unless moved")

## Recap slide ("Where Lab 5 Fits") — update inputs/outputs

- **Recap · Lab 4** needs to change from "single agent loop, resolve/escalate" to what Lab 4
  *actually* currently teaches per `lab4-standalone/README.md`: implement a scoped fix
  (`stock_split_adjustment`) against a failing test, then delegate to a **pre-built,
  project-scoped, read-only** subagent (`strategy-reviewer`) for independent review before
  wiring it in — i.e., Lab 4 is where "Skill vs. subagent" and "a subagent you're handed" first
  appear. (Ground this in `lab4-standalone/README.md`, not in `lab4-deck`'s current slides — see
  the out-of-scope note below on why those two currently disagree.)
- **This lab** bullets need to change from "orchestrator + subagents, model right-sizing,
  prefix caching, eval harness" to "author your own personal subagent, confirm proactive +
  explicit delegation, measure context savings, map transitive impact."
- **Next** bullet pointing at Lab 6 should describe it accurately as a **demo**, not another
  hands-on ticket lab — the current agenda has Lab 6 as "DevX MCP Demo" (12:30–13:30, a Wells
  Fargo employee demo), not a lab with its own backlog ticket. Don't overstate it as "Lab 6
  packages this as a slash command" (that was the old Lab 6 framing tied to the old Lab 5) unless
  that's reconfirmed against `lab6-deck`'s own current content.

## The "Pattern" slide — R→D→A→O may not fit cleanly this time

Every earlier deck (Lab 4, old Lab 5) hangs its "Pattern" slide on the Read → Decide → Act →
Observe loop, because each of those labs *is* a runtime agent loop. Lab 5's new content isn't a
runtime loop over a batch — it's four sequential lab **parts**: Orient (skim six files) → Build
(author the subagent) → Confirm delegation (proactive, then explicit) → Produce the note
(verify with the checker). Two options, pick one when implementing:
- Drop R→D→A→O for this section and use a 4-part pattern table instead (Orient/Build/Confirm/
  Produce), OR
- Keep R→D→A→O but reframe it at the *engineer's* level rather than the code's: Read (skim the
  six files), Decide (does this need a subagent, and which scope), Act (author + delegate),
  Observe (check `/usage` delta, verify the note) — consistent with the loop motif but honest
  about what's actually happening.
Recommend the first option — forcing the loop onto a lab that isn't runtime-iterative risks
diluting what the loop means everywhere else it's used.

## Code examples to source

- The call graph itself: `get_price` → (`current_weights`, `compute_trades`, `advisory_fee`) →
  (`check_drift`, `build_statement`) — a good visual for "direct vs. transitive," reusing the
  `category-grid`/`bench-table` patterns already established in other decks.
- The subagent-creation prompt from README Part 2 (the one that specifies `name`, the tracing
  job, `tools: Read, Grep, Glob`, `model: Sonnet`) as a "code example" slide, since there's no
  pre-written subagent file to show — the learner's own prompt *is* the artifact here.
- `check_impact_note.py`'s `DIRECT_CALLERS` / `TRANSITIVE_CALLERS` lists as the verifiable
  target — short, deterministic, good contrast to a "read it yourself and hope" judgment call.

## MCQ sourcing (map one question per objective)

1. Why does `change-impact-mapper` belong at `~/.claude/agents/` rather than checked into this
   project's `.claude/agents/`? (→ tracing callers is a habit for every codebase, not a rule
   specific to this one; contrast with `strategy-reviewer`'s project scope in Lab 4.)
2. What's the most common reason a subagent doesn't get proactively delegated to? (→ a vague
   `description` that doesn't match the task — not a permissions or tools problem.)
3. What does delegating the six-file trace to a subagent save that reading them inline in the
   main conversation doesn't? (→ the subagent's own reasoning happens in an isolated context
   window; only its summary re-enters the main conversation's context.)
4. Why does a change-impact note need to name `build_statement` even though it never mentions
   pricing in its own body? (→ it's a transitive dependency through `advisory_fee` /
   `compute_trades` / `check_drift` — exactly what a keyword search on `get_price(` would miss.)

## Out of scope for this pass, but worth a follow-up check

- **`lab4-deck` is itself significantly stale**, independent of anything Lab 5 does. Its current
  slides never mention `strategy-reviewer`, the Skill-vs-subagent decision point, or a review
  step at all — instead they cover an "ORCL / `triage_with_claude`" model-driven-Decide beat that
  doesn't appear anywhere in the current `lab4-standalone` package. This is a bigger rebuild than
  Lab 5's and deserves its own pass; flagging so whoever writes Lab 5's "Recap · Lab 4" slide
  knows to source it from `lab4-standalone/README.md` directly rather than from `lab4-deck`'s
  current (stale) content.
- **The orchestrator-worker/context-isolation term currently lives only in the just-rebuilt
  `lab7-deck`**, phrased as "Lab 4 taught independence... this lab adds context isolation."
  If Lab 5's rebuild introduces that vocabulary first (chronologically it precedes Lab 7), Lab
  7's phrasing should probably shift to credit Lab 5 instead of Lab 4 for the context-isolation
  half of that framing. Not fixed here since it touches an already-shipped deck — worth a
  short follow-up edit once Lab 5 ships.
- **`lab6-deck`'s own recap ("Recap · Lab 2")** doesn't reference Lab 5 at all currently, so
  there's no existing wrong claim to contradict — but once Lab 5 ships, double-check whether
  `lab6-deck` should gain a "Recap · Lab 5" callback given Lab 5 now sits immediately before it
  on the agenda. Not fixed here.
- The rebuild itself: after editing `sections/01-.../slides.html`, run
  `python3 scripts/build_deck.py --deck lab5-deck` from `training-materials/staging/` (and a
  full `python3 scripts/build_deck.py` if `deck.json`'s `summary` changes, since the top-level
  landing page tile is generated from it too) — don't hand-edit the generated `index.html` files.
