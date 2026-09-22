Lab 1 — Foundations / WM-101 fix
Deck objectives: describe the Read→Decide→Act→Observe loop; write a 5-ingredient frame; ship one verified change backed by test evidence.
README does: score prompts, refine MY_FRAME to 9/10, fix WM-101 with scoped-bugfix-flow, hand back test evidence.
In sync? Yes. Frame-writing and verified-change objectives are directly exercised; the loop is a lecture concept. Minor: the deck objective "name a task where an agent adds value and one where it doesn't" is discussion-only, never a lab artifact — fine to leave, but it's an objective with no lab step behind it.

Lab 2 — Two-pass Skills
Deck objectives: use built-in tools (Glob/Grep); use an existing generic Skill; author your own fee Skill and invoke it; distinguish built-in vs downloadable vs self-authored.
README does: Pass 1 generic Skill on quarterly; Pass 2 author a fee-standardization Skill for monthly; deliverable includes both Skill artifacts + comparison.
In sync? Strong — and this is your model for honest verbs. Learners genuinely author here, and the objective says "author." Only soft gap: objective 1's explicit Glob/Grep habit isn't called out as a required step in the README (it's implied / optional context exercise).

Lab 3 — Plan Mode & TDD
Deck objectives: explain Plan mode; use a failing test as spec; describe analyze→plan→implement→verify→deliver; recognize when a verified criterion improves the plan.
README does: Parts 1–5 walk that exact flow on WM-110 hysteresis; Part 6 stretch has them write the test first.
In sync? Yes, tight. Part 6 actively deepens objective 4 (learner writes the spec). No gap.

Lab 4 — Implement + independent review
Deck objectives: reframe a vague ticket + implement a scoped fix against a failing test; explain what a subagent is; decide Skill-vs-subagent; delegate to a pre-built, read-only subagent and act on CHANGES NEEDED.
README does: implement stock_split_adjustment against a failing test; delegate to the pre-built strategy-reviewer.
In sync? Yes — and notably the objective honestly says "pre-built" and "delegate," which matches learners using (not authoring) the subagent. Good precedent for how to word Lab 7.

Lab 5 — Author your own subagent
Deck objectives: author a personal-scoped subagent; distinguish personal vs project scope; confirm proactive vs explicit delegation; measure context savings; produce a direct+transitive impact note.
README does: author change-impact-mapper; confirm both delegation modes; produce impact_note.md verified by check_impact_note.py.
In sync? Mostly strong — learners do author. One gap: objective 4 says "Measure, not just assert" the context savings, but in the README that measurement is an Optional step. Either promote it to a required step or soften the verb to "observe/estimate."

Lab 7 — Structured logging (the one you flagged)
Deck objectives: explain why a cross-cutting workflow is worth packaging as a Skill + identify which step deserves a subagent; "Compose a Skill and a subagent in one workflow"; distinguish independence-delegation vs context-saving delegation; read a SKILL.md phase flow and identify the delegable phase; explain what a PreToolUse hook enforces.
README does: learner uses the pre-built structured-logging-rollout Skill, delegates to the pre-built logging-reviewer subagent, and confirms the pre-built hook blocks an off-scope edit. They thread logging through three files. They author none of the three artifacts.
In sync? This is the real gap, and your instinct is right:

Objective 2 ("Compose a Skill and a subagent") is the mismatch. "Compose" reads as author/assemble, but learners only invoke a pre-built Skill that already delegates to a pre-built subagent. Every other objective in this deck uses honest verbs (explain / identify / read / distinguish) — objective 2 is the outlier.
Objectives 1, 3, 4, 5 are analysis/explanation verbs that the README does support (Part 2 "why a Skill," Part 3 "why a subagent here," Part 4 the hook). Those are fine.
Recommendation for Lab 7: reword, don't add build work. Change objective 2 to match Lab 4's honest phrasing, e.g. "Use a Skill and a subagent together in one workflow — a Skill that implements inline and delegates its own review to a subagent." Reasons:

The 13:30–14:45 slot already has learners thread a multi-file change; adding author-the-Skill + author-the-subagent + author-the-hook would overload it and duplicate what Labs 2 and 5 already teach (authoring a Skill; authoring a subagent).
Lab 7's genuinely new teaching point is composition/orchestration + hook-as-enforcement, not authoring. The objective should name that.
Same wording bug appears in two more places you'll want to fix in the same pass: the title-slide subtitle ("Compose a Skill and a subagent in one workflow…") and the top-level deck card we just edited ("Compose a Skill, a subagent, and protective hooks…"). "Compose" overstates in all three.
Optional stretch (if you want some authoring): have them add one protected region to protected_regions.json, or extend the Skill's reference.md — small, in-scope, and reinforces the hook/Skill mechanics without a full build.
Lab 8 — Capstone
Deck objectives: run two read-only subagents in parallel; cross-reference into a citation-backed judgment; apply the Skill-vs-subagent test cold; defend a recommendation as a verifiable target.
README does: install two pre-built subagents, fan out in parallel, synthesize my-recommendation.md, present and survive challenge.
In sync? Yes. Honest verbs ("run," not "author"), synthesis and presentation are the real work, and the objectives match.

Bottom line
Reword (verb mismatch): Lab 7 objective 2 — "Compose" → "use together / compose a workflow from." This is the one true synch gap, and it repeats in the Lab 7 subtitle and index card.
Decide required-vs-optional: Lab 5 objective 4 ("Measure" the savings) is only an optional step — promote the step or soften the verb.
Minor: Lab 2 objective 1 (Glob/Grep habit) and Lab 1's "name a task where an agent doesn't help" are stated objectives with no explicit lab step — acceptable as lecture beats, but worth knowing.
Solidly in sync, no change needed: Labs 3, 4, 8 (and Labs 1–2 substantively). Labs where learners actually author (2 and 5) correctly say "author"; labs where they use pre-built artifacts (4 and 8) correctly say "use/delegate/run." Lab 7 is the only place the verb claims more than the lab delivers.
