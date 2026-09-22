# Pre/Post Quiz: Skills, Subagents, and Context Management

Use the same 10 questions before and after training. For the pre-training quiz, ask learners to answer from current understanding only. For the post-training quiz, ask them to answer based on the course language and lab evidence.

## Learner Copy

1. In the Agentic Mindset Shift, what changes when moving from autocomplete-style assistance to agentic coding?

   A. The assistant only suggests shorter code completions.

   B. The developer delegates an outcome, the agent owns more of the approach, and the developer reviews the result.

   C. The developer stops defining verification because the agent can judge completion.

   D. The agent should be used mainly for one-line edits.

2. Which sequence best matches the core agent loop taught in the course?

   A. Prompt -> Generate -> Commit -> Deploy

   B. Plan -> Type -> Save -> Push

   C. Read -> Decide -> Act -> Observe

   D. Search -> Rewrite -> Summarize -> Archive

3. Which set contains the five ingredients of a strong task frame?

   A. Outcome, Scope, Verification, Deliverable, Guardrails

   B. Persona, Tone, Length, Examples, Deadline

   C. Files, Branch, Model, Owner, Estimate

   D. Summary, Prompt, Diff, Commit, Release note

4. In Lab 1 and Lab 2, why does the Skill need a specific frame from the user?

   A. A Skill is an on-demand workflow parameterized by the task frame, not by hidden knowledge of the ticket.

   B. A Skill can only run when every repository file has already been read into context.

   C. A Skill replaces the need for tests or acceptance criteria.

   D. A Skill always chooses its own scope and verification command.

5. When is creating a new `SKILL.md` most justified?

   A. Any time a task feels difficult or unfamiliar.

   B. When a bounded workflow is repeated and benefits from shared steps, conventions, and verification.

   C. When you need a separate context window for independent review.

   D. When the codebase has no tests.
When
6. What is the key difference between a Skill and a subagent in Claude Code as used in these labs?

   A. Skills run inline in the main conversation; subagents run in isolated context with their own tool list and model.

   B. Skills are only for documentation; subagents are only for editing code.

   C. Skills are always personal; subagents are always project-scoped.

   D. Skills can enforce read-only tools; subagents cannot.

7. Which scenario is the best candidate for a read-only subagent rather than a Skill running inline?

   A. Applying the same deterministic formatting command to one file.

   B. Reviewing a completed reconciliation strategy with fresh context and no ability to edit code.

   C. Fixing a small typo in a README.

   D. Running the exact test command named in a task frame.

8. What primarily drives proactive subagent delegation?

   A. The subagent's `description` matching the current task.

   B. The alphabetical order of files in `.claude/agents/`.

   C. Whether the user has already mentioned the subagent by name.

   D. The number of tools listed in the subagent frontmatter.

9. In Lab 5, why is tracing transitive callers a stronger context-management example than simply grepping for `get_price(`?

   A. Grep is never useful in Claude Code.

   B. Transitive callers can be affected by a change even when their own code never mentions the changed function.

   C. Transitive callers only matter after code has already been edited.

   D. Grep always reads every file into the main conversation.

10. Which statement best captures the course's guidance on managing context with Skills and subagents?

    A. Put everything into the main conversation so the agent never has to summarize.

    B. Use Skills for reusable inline workflows, use subagents when isolation, least-privilege tools, a different model, or context savings earn the overhead, and keep verification explicit.

    C. Use subagents for every repeated task because they are always cheaper than Skills.

    D. Avoid project rules like `AGENTS.md` or `CLAUDE.md` because they add context cost without benefit.

## Facilitator Answer Key

1. **B** — The mindset shift is from detail completion to outcome delegation under review.
2. **C** — The core loop is Read -> Decide -> Act -> Observe.
3. **A** — The course's five task-frame ingredients are Outcome, Scope, Verification, Deliverable, and Guardrails.
4. **A** — `scoped-bugfix-flow` and similar Skills are reusable workflows; the frame supplies the target, limits, and checks.
5. **B** — A Skill earns its keep when the workflow repeats and needs consistent conventions or checks.
6. **A** — A Skill runs inline; a subagent runs in an isolated context with its own frontmatter-defined tools/model.
7. **B** — Independent, read-only review is a core subagent use case from Labs 4 and 7.
8. **A** — Claude matches the task against each subagent's `description`; vague descriptions often fail to trigger.
9. **B** — Lab 5's point is that blast radius includes indirect dependencies a direct text search can miss.
10. **B** — This combines the main guidance: reusable inline workflows for Skills, isolation/least privilege/context savings for subagents, and explicit verification.

## Scoring Notes

- Score one point per question, 10 points total.
- Treat a post-training score of 8 or higher as evidence that learners can distinguish the major Claude Code workflow primitives.
- Compare pre/post deltas by topic: questions 1-3 cover mindset and framing, 4-5 cover `SKILL.md`, 6-8 cover subagents, and 9-10 cover context management.