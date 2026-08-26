# Writing a Solid `prd.json` for Ralph Loop Work

A practical guide for product-minded engineers who want autonomous AI loops (Ralph, Ralph Zero, ralph-claude-code, ralph-copilot, etc.) to actually *finish* work without thrashing.

> **TL;DR** — A `prd.json` is the steering wheel of a Ralph loop. The agent reads it on every iteration, picks one task, implements it, marks it done, and exits. If the file is sloppy, the loop is sloppy. The hardest part of writing a good `prd.json` is **everything you do before you open the file.**

---

## 1. Context: what Ralph is and why `prd.json` matters

Ralph (Geoffrey Huntley's "Ralph Wiggum technique") is a deliberately simple pattern: a bash loop restarts a coding agent (Claude Code, Amp, Cursor CLI, etc.) over and over with a fresh context window. State lives on disk — typically `PROMPT.md`, `AGENTS.md`, `specs/*`, an `IMPLEMENTATION_PLAN.md`, and a `prd.json` (or equivalent task ledger).

Each iteration the agent:

1. Loads the same files deterministically.
2. Picks **one** unfinished task.
3. Investigates the codebase, implements, runs tests/typechecks/lints (the "backpressure"), commits.
4. Updates the task's status and exits.
5. The bash loop restarts immediately with a clean context.

`prd.json` is the durable, machine-readable list of work that survives across these resets. It is **not** a free-form design doc — it is a queue of atomic, verifiable tasks. The quality of this file determines whether the loop converges or circles forever.

---

## 2. PRD vs. BRD vs. MRD — and why this matters before you write JSON

These three documents look similar but answer different questions. A Ralph `prd.json` is the *last* of them, not the first. Skipping the upstream work is the most common reason loops fail.

| Document | Question it answers | Audience | Owner | Lives at |
|---|---|---|---|---|
| **MRD** — Market Requirements | *Should we build this at all?* — market size, demand, competitors, customer evidence | Exec / GTM / investors | Product marketing | Slides, market research, Notion |
| **BRD** — Business Requirements | *Why is the business doing this, and what does success look like commercially?* — goals, KPIs, constraints, budget, deadlines, risks | Leadership / sponsors | Business owner / PM | Confluence, Google Docs |
| **PRD** — Product Requirements | *What must the product do, for whom, with what acceptance criteria?* — features, user stories, scope, non-goals | Engineering, design, QA | Product manager | Markdown spec → `prd.json` |

The natural sequence is **MRD → BRD → PRD → `prd.json`**. Each step narrows the scope:

- The **MRD** decides the bet is worth making.
- The **BRD** translates that bet into measurable business outcomes and constraints (budget, time-to-market, regulatory, etc.).
- The **PRD** translates those outcomes into concrete product behavior — personas, user stories, acceptance criteria, in-scope vs. out-of-scope.
- The **`prd.json`** translates the PRD into atomic, machine-executable tasks for an autonomous agent.

> Ralph cannot recover from a bad MRD or BRD. If the *thing* is wrong, no amount of green tests will save you. The loop will faithfully build the wrong product.

In modern lean teams these three frequently collapse into a single document, but the *thinking* must still happen — you just consolidate the artifacts.

---

## 3. Pre-PRD work: the part nobody wants to do (and the reason loops fail)

This is the section to read twice. Ralph amplifies whatever you feed it. If your inputs are vague, you get a vague product, fast and at scale.

### 3.1 Validate the problem (MRD-level work)

Before any JSON:

- **Who hurts and how much?** Name 3–5 real users, their role, their current workaround, and what the pain costs them (time, money, errors).
- **Is there a market or just a hobby?** Estimate users × frequency × willingness to pay (or strategic value, for internal tools).
- **What already exists?** List 3+ alternatives (build, buy, do nothing) and why they fall short.
- **What evidence do you have?** Interviews, support tickets, analytics, churn reasons. "I think users would like…" is not evidence.

Output: a one-page problem statement. If you can't write one, you are not ready.

### 3.2 Frame the business case (BRD-level work)

- **Goals**: 2–4 measurable outcomes ("reduce onboarding time from 14 to 3 days", "cut support tickets in category X by 40%"). Define them *before* building, not after. Mix quantitative metrics with qualitative ones (e.g. "users describe the flow as 'painless' in interviews").
- **Appetite / investment** (from Olivier Courtois's Bet Template, an idea borrowed from Shape Up): if you were the investor, how many work-days are you willing to spend on this *specific* problem before re-evaluating? Naming a budget upfront forces ruthless prioritisation and prevents the loop from running indefinitely.
- **Constraints**: budget, deadlines, compliance, security, headcount, stack lock-ins.
- **Pre-mortem (risks & assumptions)**: imagine the project failed — write the post-mortem now. What technical unknowns, design ambiguities, interdependencies, or operational tasks killed it? For each, note a mitigation. This is much cheaper than a real post-mortem.
- **Success and failure thresholds**: at what number do you double down, and at what number do you kill it? A useful failure threshold is the inverse of the Sean Ellis test: *"fewer than 40% of beta users would be 'very disappointed' to lose this — kill or pivot."*
- **Stakeholders**: who must approve, who must be informed, who must integrate.

### 3.3 Discovery: get sharp on users and scope

Three frameworks worth running through before opening any editor:

**Universal Idea Model** — fill this in cleanly or you are not ready:

> An *[object]* for *[class of users]* that *[does X]* in order to *[achieve Y]*. Users benefit by *[gain]* when *[situation]*.

If any blank is fuzzy, stop and go back to discovery.

**Problem Framing**:

- Environment — who is affected, who are the stakeholders?
- Dynamics — when did this emerge, how has it evolved?
- Current state — symptoms vs. root causes?
- Ideal state — what does success look like in concrete behavior?

**Product Concept (six dimensions)** — context, users & needs, form factors, strategy & execution, monetisation, open questions.

### 3.4 Sharpen personas

Replace "users" with named, specific personas. "Busy working parent who manages family logistics on a phone between meetings" beats "productivity-focused user". Each persona gets: role, goals, frustrations, context of use, level of technical skill.

### 3.5 Define what is **out of scope**

This is the single most under-used section in real-world PRDs and the one that saves Ralph from wandering. Every feature you do not explicitly exclude becomes implicit scope creep the moment the agent starts inferring.

For each tempting-but-deferred feature, write one line: *what* is excluded, *why now*, *when reconsidered*.

### 3.6 Decide architecture and conventions *before* the loop runs

Ralph imitates the code it sees. Whatever exists in the repo on iteration 0 will shape every subsequent iteration. So:

- Pick the stack, framework versions, and language conventions deliberately.
- Add seed files: a single working endpoint, one passing test, one CI run, the chosen lint config.
- Author `AGENTS.md` (≤ 60 lines) with the actual build/test/typecheck/lint commands. Not a changelog — an operating manual.
- Decide commit style, branch naming, PR rules.

This is **upstream steering**: cheap to do once, impossible to retrofit cleanly.

### 3.7 Two PRD templates worth studying

Two public templates compress most of the wisdom above into one-page formats and are worth borrowing from before you ever write JSON:

**Kevin Yien's PRD template (Square)** — a lean, gated, three-act structure:

1. **Problem Alignment** — Problem (1–2 sentences), High-level approach, Narrative (optional storytelling), Goals, **Non-goals**. Ends with a sign-off table; do not continue until reviewers literally sign.
2. **Solution Alignment** — Key features (Plan of Record + Future Considerations), Key flows, **Key logic** (rules and edge cases written out as text instead of being inferred from designs). Ends with a second sign-off table.
3. **Launch Plan** — Key milestones with **exit criteria** for each phase (Pilot → Beta → Early Access → Launch). The Beta exit criterion is a Sean Ellis test in disguise: *"At least 10 customers would be disappointed if we took it away."* Plus an **Operational Checklist** across Analytics, Sales, Marketing, CS, PMM, Partners, Globalization, Risk, and Legal.
4. **Appendix** — Changelog, Open Questions, FAQs, Impact Checklist (Permissions, Reporting, Pricing, API, Global).

The high-leverage ideas: explicit sign-off gates between phases, named exit criteria per milestone, an operational sweep across non-engineering teams, and a section reserved purely for non-goals.

**Olivier Courtois's Bet Template (Productverse / Comet)** — even leaner, framed around bets:

- **Problem Alignment** — Problem, **Success measures** (quantitative + qualitative, tied to the north-star metric), **Investment / appetite** (PM-as-investor: how many work-days?).
- **Solution Alignment** — Bet (lean, testable solution), Risks & assumptions / pre-mortem, **No-gos** (explicit out-of-scope).
- Notes block carrying three rules worth tattooing on the wall: write in plain English with no codenames; the PM owns the bet but the developer and designer own the solution and details; *"build the right thing, then build the thing right."*

The high-leverage ideas: every solution is a *bet*, not a commitment; investment caps the loop's runtime; no-gos are a first-class section; "right thing first, right way second" — Ralph cannot reorder these.

For a `prd.json`, you do not need to copy either template wholesale, but the sign-off table, exit criteria, operational checklist, appetite, pre-mortem, and explicit no-gos all earn their keep — write them in the markdown PRD upstream and they will translate cleanly into stricter `description`, `acceptanceCriteria`, and `effort` values in the JSON.

### 3.8 Wire backpressure

Ralph only stays honest if reality pushes back. Before the first loop:

- Tests must run with one command and exit non-zero on failure.
- Typecheck and lint must do the same.
- For subjective criteria (tone, UX), prepare an LLM-as-judge with a binary pass/fail rubric.
- Make sure the agent cannot "succeed" by deleting failing tests — protect critical tests, or add a guard in the prompt.

If you cannot articulate "how does Ralph know it failed?" for every task, the task is not ready.

---

## 4. The `prd.json` schema

The exact shape varies by Ralph fork, but the canonical structure (per `snarktank/ralph`'s `prd.json.example`) is:

```json
{
  "project": "task-priority-system",
  "branchName": "feature/task-priority",
  "description": "Add a three-level priority system to tasks with UI indicators, editing, and filtering.",
  "userStories": [
    {
      "id": "US-001",
      "title": "Add priority column to tasks table",
      "description": "As a backend, I need a priority field on the tasks table so the rest of the feature can read and write it.",
      "acceptanceCriteria": [
        "Migration adds `priority` (enum: low, medium, high) to `tasks` with default 'medium'",
        "Existing rows get backfilled to 'medium'",
        "`bun run typecheck` passes",
        "`bun run test:db` passes including a new test asserting the default value"
      ],
      "priority": 1,
      "effort": 0,
      "deps": [],
      "passes": false,
      "notes": "No API change in this story."
    },
    {
      "id": "US-002",
      "title": "Show priority indicator on task card",
      "description": "As a user viewing my task list I want a colored dot on each card so I can scan priorities at a glance.",
      "acceptanceCriteria": [
        "Card renders a dot: red=high, amber=medium, grey=low",
        "Component story exists and snapshots the three states",
        "Verify in browser using the dev-browser skill: list page shows three dots correctly"
      ],
      "priority": 2,
      "effort": 0,
      "deps": ["US-001"],
      "passes": false
    }
  ]
}
```

### Root fields

| Field | Type | Purpose |
|---|---|---|
| `project` | string | Human label, used in commit messages and logs |
| `branchName` | string | Git branch the loop commits to |
| `description` | string | One paragraph explaining the *why* of this batch — read on every iteration, so keep it tight |
| `userStories` | array | Ordered list of atomic tasks |

### User-story fields

| Field | Type | Required | Purpose |
|---|---|---|---|
| `id` | string | yes | Stable identifier (`US-001`); never renumber |
| `title` | string | yes | One short imperative sentence |
| `description` | string | yes | "As a *[persona]*, I want *[action]* so that *[outcome]*" |
| `acceptanceCriteria` | string[] | yes | Concrete, testable statements — see §6 |
| `priority` | number | yes | 1 = do first; ties broken by `id` order |
| `effort` | number | recommended | 0 = atomic, 1 = multi-file, 2 = risky/ambiguous (split before running) |
| `deps` | string[] | recommended | IDs of stories that must be `passes: true` first |
| `passes` | boolean | yes | The loop's exit condition; starts `false`, agent flips to `true` |
| `notes` | string | optional | Hints, links, gotchas — not requirements |

If your fork uses different field names, keep the **shape** of the contract: id, intent, acceptance, dependency, status.

---

## 5. Task granularity: the single most important property

A Ralph task must fit comfortably inside **one context window**. Not "a sprint", not "a feature" — a single, restartable unit of work.

**Right-sized**:

- Add a database column + migration + one test.
- Add a filter dropdown to an existing list page.
- Wire a new endpoint that calls an existing service method.
- Replace a hardcoded string with a config value across known files.

**Too big** (split immediately):

- "Build the dashboard."
- "Add authentication."
- "Implement the export feature."

**Heuristic**: if you cannot write 3–6 acceptance criteria that are *all* mechanically checkable, the task is too big or too vague. Split it.

A separate symptom of oversized tasks: the loop "fixes" tests over and over. That is the agent gaming an ambiguous spec, not making progress. Stop the loop and tighten the criteria.

---

## 6. Writing acceptance criteria that drive backpressure

Acceptance criteria are not aspirations. They are the contract the agent and the test runner will be measured against. Each criterion should be one of:

- **Mechanical** — a command and its expected exit code or output. *"`bun run typecheck` passes."*
- **Behavioural** — a specific, observable user-visible outcome. *"Submitting an empty form shows the inline error 'Email is required' under the input."*
- **Verifiable in browser** — for frontend work, name the skill/tool and the page. *"Verify in browser using the dev-browser skill: `/tasks` page renders 3 colored dots."*
- **Negative** — an outcome that must *not* occur. *"No new dependencies are added to `package.json`."*

Avoid: "works well", "is performant", "looks good", "handles edge cases". Replace with measurable equivalents or move to a separate evaluation story.

State **what to verify, not how to build it.** Implementation prescriptions ("use a `useMemo` here, place the button 20px from the top right") belong in design specs or code review, not in the PRD. Over-specifying implementation removes Ralph's ability to use the codebase's existing patterns and makes the spec brittle.

---

## 7. Workflow: from idea to `prd.json`

A reliable pipeline used by most Ralph forks:

1. **Discovery** (§3) — produce a one-page problem statement, persona list, success metrics, and out-of-scope list.
2. **Markdown PRD** — write `tasks/prd-<feature>.md` with sections: Overview, Personas, Goals & Metrics, In Scope, Out of Scope, User Stories (epic level), Acceptance Criteria, Assumptions & Constraints, Open Questions.
3. **Cross-functional review** — share the markdown draft. Ten minutes silent reading, then collect what is missing, wrong, or unvalidated. *Sharing drafts inviting improvement, not finals inviting approval.*
4. **Convert to `prd.json`** — split each user story into atomic tasks with concrete acceptance criteria. Many forks ship a `/ralph` or `/prd` skill that does this conversion; whether you use it or not, *review every entry by hand*.
5. **Dry-run a single iteration** — execute one loop iteration manually. Read the diff, the commit, the test run. Tune `AGENTS.md` and the prompt before letting it run unattended.
6. **Run the loop** — observe the first 3–5 iterations live. Then move outside the loop and let it grind.

---

## 8. Common failure modes (and how to spot them in the JSON)

| Symptom in the loop | Likely cause in `prd.json` | Fix |
|---|---|---|
| Agent edits and re-edits the same file | Two stories overlap or contradict | Merge or sequence with `deps` |
| Tests get deleted or skipped | Acceptance criterion is "tests pass" with no scope | Name the specific tests/files; add a "no test deletions" criterion |
| Loop circles, never converges | Stories too big | Split until each is `effort: 0` |
| Implementation drifts from intent | Description is a feature title, not a user story | Rewrite as "As… I want… so that…" |
| Out-of-scope features appear | No `nonGoals` / out-of-scope section in `description` | Add explicit exclusions to `description` |
| Agent invents personas or metrics | PRD upstream was vague | Go back to §3, do not patch in JSON |
| "Done" but the product is wrong | Success metrics never wired to acceptance criteria | Tie at least one criterion per epic to a measurable business outcome |

---

## 9. Quality signals — is this `prd.json` ready?

Before starting the loop, the file should pass all of these:

1. **An engineer can estimate every story** without asking questions.
2. **A designer can prototype every UI story** from the description alone.
3. **Every acceptance criterion is mechanically or visually checkable.**
4. **The out-of-scope list surprises nobody** on the team.
5. **No story is `effort: 2`** — anything risky is split, spiked, or moved to a separate phase.
6. **`AGENTS.md` lists the exact commands** referenced in acceptance criteria.
7. **The first story is independently shippable** if the loop is killed after one iteration.

If any of these fail, you are not ready to start the loop. Iteration on the spec is much cheaper than iteration on bad code.

---

## 10. The PRD is a living document

Ralph runs for hours or days. Reality changes:

- A user story turns out to be infeasible — mark it `passes: true` with a `notes` explaining why, or remove it and add a replacement.
- Discovery during a build reveals a missing prerequisite — add a new story and reorder `priority`.
- Backpressure flags a recurring failure — add a global guardrail to `description` rather than repeating it in every story.
- Plans go stale — regenerate. The cost of one planning iteration is small compared to letting Ralph circle.

Treat `prd.json` like source code: small commits, clear messages, and never edit while the loop is running unless you are deliberately steering it. Keep a **changelog** at the top of the upstream markdown PRD — date, change, who decided — so the spec is auditable. Bake the mantra in: *build the right thing, then build the thing right.* The loop is very good at the second; the changelog is your evidence that you are still doing the first.

---

## 11. Minimum viable checklist

Before you press Go on the loop:

- [ ] One-page problem statement validated with ≥3 real users
- [ ] Goals and failure thresholds written down
- [ ] Universal Idea Model fully filled in
- [ ] Named personas (not "users")
- [ ] Explicit out-of-scope list
- [ ] Stack, conventions, seed files in place
- [ ] `AGENTS.md` with real build/test/lint commands
- [ ] Backpressure (tests, typecheck, lint) green on `main`
- [ ] Markdown PRD reviewed by engineering and design
- [ ] `prd.json` with `effort: 0` on every story, real acceptance criteria, declared `deps`
- [ ] One manual iteration run and reviewed diff-by-diff
- [ ] Sandboxed environment (no creds, no SSH keys exposed)
- [ ] Sign-off recorded from engineering + design + (where relevant) PMM, support, legal, security
- [ ] Operational sweep done: analytics tracking, support content, GTM, partners, globalisation, risk/legal — flagged or NA, not silent
- [ ] Appetite agreed: maximum work-days before the loop is paused for human review
- [ ] Document is in plain English — no codenames, no internal jargon a fresh agent would have to guess

When all sixteen are checked, start the loop and step outside it.

---

## Sources & further reading

- [Ralph: autonomous AI agent loop until all PRD items are complete (snarktank/ralph)](https://github.com/snarktank/ralph)
- [How to Ralph Wiggum — Geoffrey Huntley](https://github.com/ghuntley/how-to-ralph-wiggum)
- [Inventing the Ralph Wiggum Loop — Dev Interrupted](https://devinterrupted.substack.com/p/inventing-the-ralph-wiggum-loop-creator)
- [The Ralph Loop: When Your PRD Becomes the Steering Wheel — Valentin Nagacevschi](https://medium.com/@ValentinNagacevschi/the-ralph-loop-when-your-prd-becomes-the-steering-wheel-5abf6b1345c0)
- [Ralph — Ry Walker Research](https://rywalker.com/research/ralph)
- [Ralph Zero — orchestrator over Ralph (davidkimai/ralph-zero)](https://github.com/davidkimai/ralph-zero)
- [ralph-claude-code (frankbria)](https://github.com/frankbria/ralph-claude-code)
- [ralph-copilot (giocaizzi)](https://github.com/giocaizzi/ralph-copilot)
- [PRD Writing Best Practices — Ainna](https://ainna.ai/resources/faq/prd-guide-faq)
- [Figma's approach to Product Requirement Docs — Yuhki Yamashita on Coda](https://coda.io/@yuhki/figmas-approach-to-product-requirement-docs/prd-name-of-project-1)
- [PRD Template — Kevin Yien (Square)](https://docs.google.com/document/d/1mEMDcHmtQ6twzNlpvF-9maNlAcezpWDtCnyIqWkODZs/edit)
- [Bet Template — Olivier Courtois (Productverse / Comet)](https://docs.google.com/document/d/1QI7QX0ARPUeYklOKouEpeEr5AcnkUdcr6tkm1n8dV_A/edit)
- [Understanding PRD, BRD, MRD, and SRD — Findernest](https://www.findernest.com/en/blog/understanding-prd-brd-mrd-and-srd-a-quick-guide)
- [BRD vs. MRD — Blackblot](https://www.blackblot.com/brd-versus-mrd)
- [Breaking Down BRD, PRD, SRD, and MRD — Brucira](https://blog.brucira.com/breaking-down-brd-prd-srd-and-mrd/)
- [What is a Product Requirements Document — Airtable](https://www.airtable.com/articles/product-requirements-document)
- [Product Requirements Document: Templates and Examples — AltexSoft](https://www.altexsoft.com/blog/product-requirements-document/)
