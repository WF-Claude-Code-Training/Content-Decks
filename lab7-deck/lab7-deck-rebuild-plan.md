# Lab 7 deck rebuild — teaching points to add

**For a separate run.** This is a plan, not an implementation — no deck files have been
touched. Source of truth for all content below: [`lab7-standalone/README.md`](../../../claude-labs-ttt/lab7-standalone/README.md),
[`AGENTS.md`](../../../claude-labs-ttt/lab7-standalone/AGENTS.md), the Skill at
`lab7-standalone/.claude/skills/structured-logging-rollout/SKILL.md`, and the new subagent at
`lab7-standalone/.claude/agents/logging-reviewer.md`.

## Top finding: `lab7-deck` currently covers the wrong lab

`training-materials/staging/lab7-deck/deck.json` and its one section
(`01-enforced-compliance-controls`) still describe the **old** Lab 7 — "Enforced Compliance
Controls" (WM-113, PreToolUse/PostToolUse hooks, PII redaction). That lab moved to
`claude-labs-ttt/docs/appendix-governance-hooks/` a while ago; the current Lab 7 is **WM-109 —
structured logging**, and the deck was never updated to follow it. This isn't a small addition
of teaching points — it's a **full content swap** for the one section this deck has, plus a new
title/subtitle/summary in `deck.json`.

Recommend: rename the section to something like `01-structured-logging-rollout` (update
`deck.json`'s `sections` entry and slug), rather than patching hook/PII slides in place.

## New teaching points this lab introduces (not covered by any earlier deck)

1. **A Skill's own phase flow can delegate a step to a subagent.** Every subagent use the
   course has shown so far was triggered by the *user's* prompt (Lab 4: "have strategy-reviewer
   review this"; Lab 5: orchestration code fans out several). Lab 7 is the first place a
   **Skill's own `SKILL.md`** names the delegation as one of its phases (`Phase C` in
   `structured-logging-rollout/SKILL.md`) — the engineer never has to remember to ask for
   review separately; it's part of the workflow they invoked. Worth a slide contrasting all
   three call-sites as a small ladder:
   - Lab 4 — engineer invokes a subagent directly, by name.
   - Lab 5 — orchestration code fans out N subagents in parallel.
   - Lab 7 — a Skill's own phase flow invokes one subagent as part of what "using the Skill"
     means.

2. **Skill vs. subagent is a "does this step need isolation?" question, not a power ranking.**
   Reuse Lab 4's framing (a Skill runs inline/cheap; a subagent earns its overhead through
   independence and enforced tool restriction) but add the decision test this lab makes
   concrete: Phase B (implementation) stays a Skill because the work is **fully specified in
   advance** — `reference.md` already pins every event name/field, so there's no judgment call
   to isolate. Phase C (review) moves to a subagent because independent judgment — a fresh
   reader with no stake in the code — is exactly what's being bought.

3. **Context isolation as a second, distinct reason to delegate — not just independence.**
   Lab 4 taught "subagent = independence + enforced read-only tools." Lab 7 adds a second,
   separate justification worth its own slide: a subagent's own reading/reasoning happens in an
   **isolated context window** and never bloats the parent conversation's context. This matters
   most exactly when the reviewed work spans multiple files — `logging-reviewer` reads three
   modules' worth of diff, and only a short verdict returns to the main session. Name-drop the
   industry term if useful for credibility: this is the **orchestrator-worker** pattern from
   Anthropic's own multi-agent-systems engineering writeup — parallel/independent context
   windows, condensed reports back to the orchestrator.

4. **The caveat that makes delegation safe here.** Subagents can't ask clarifying questions
   mid-task — they run to completion on the brief they're given. Delegating Phase C is only
   safe *because* `reference.md`'s conventions already removed the ambiguity a reviewer would
   otherwise need to ask about. Good pairing with point 2 — frame it as "when is delegation
   safe" versus "when is delegation possible."

5. **Not every subagent is a reviewer of *new* code — this one reviews a cross-cutting change.**
   `strategy-reviewer` (Lab 4) reviews one function against a fixed rubric. `logging-reviewer`
   reviews the *same kind of change* (structured logging) applied to three unrelated modules in
   one pass — a good moment to point out the reviewer's checklist stays stable (event naming,
   what-not-to-log, no PII, nothing else changed) precisely because the Skill's `reference.md`
   is the shared contract both the implementer (the Skill) and the reviewer (the subagent) read.

## Objectives slide — suggested rewrite

Replace the current hook/PII-redaction objectives with something like:
- Explain why a repeated, cross-cutting workflow (thread logging through N modules) is worth
  packaging as a Skill, and identify which of its steps still deserves a subagent instead.
- Compose a Skill and a subagent in one workflow: implement inline, review in isolation.
- Distinguish "delegate for independence" (Lab 4) from "delegate to save context on multi-file
  work" (this lab) as two different, both-legitimate reasons to reach for a subagent.
- Read a `SKILL.md` phase flow and identify which phase is a candidate for subagent delegation,
  and why (fully-specified vs. judgment-requiring work).

## Metadata updates needed in `deck.json`

- `title`: "Lab 7 — Add Structured Logging" (drop "Enforced Compliance Controls")
- `subtitle`: something like "Compose a Skill and a subagent: implement inline, review in
  isolation"
- `summary`: replace hook/PII summary with the WM-109 structured-logging-rollout summary
- Ticket badge: `WM-113` → `WM-109`
- Keep the Day 2 / 13:30–15:00 timing block as-is unless the agenda has since moved this lab

## Recap slide ("Where Lab 7 Fits") — update inputs/outputs

- **Recap · Lab 6** stays the same (`/frame-backlog` via MCP).
- **This lab** bullets need to change from "hooks — block, redact, log" to "compose a Skill +
  a subagent for a cross-cutting, multi-file audit-logging rollout."
- **Next** bullet pointing at Lab 8 should stay conceptually similar (governed CI/CD) but check
  it doesn't still reference hook-enforcement as the throughline from Lab 7 into Lab 8.

## Out of scope for this pass, but worth a follow-up check

- `lab4-deck` and `lab5-deck` may not yet reflect that `strategy-reviewer` (a subagent) is
  introduced in **Lab 4**, not Lab 5 — `lab4-deck/sections/01-agent-loop-and-first-agent`
  currently reads "Lab 5 scales this from one agent to orchestration and subagents," which
  undersells that Lab 4 already has a subagent. Not fixed here; flagging so the ladder slide in
  point 1 above doesn't contradict whatever lab4-deck/lab5-deck end up saying.
- The rebuild itself: after editing `sections/01-.../slides.html`, run
  `python3 scripts/build_deck.py --deck lab7-deck` from `training-materials/staging/` per
  `SKILL-rebuild-deck.md` — don't hand-edit the generated `index.html` files.
