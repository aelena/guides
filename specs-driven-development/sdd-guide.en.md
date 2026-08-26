# Spec-Driven Development

### A short guide to governing change when a model writes the code

**Version 0.2 · Draft · August 2026**

> This guide is a synthesis from multiple sources, not original research. 
> Sources listed at the end. Where I disagree with a source I say so.

---

## What this guide is for

You can now describe a feature in a sentence and get working code in seconds.
That capability is real and it is not going away. What it does not give you is a
way to answer, six weeks later, why the system behaves as it does, which of those
behaviours anyone actually agreed to, and what will tell you if the next change
breaks one of them.

This guide is about closing that gap without giving up the speed. It is short on
purpose. If you want the full treatment, the sources at the end are better than a
summary of them.

**The running example** throughout is a loyalty promotion: a campaign that
triples a customer's points balance, capped at a maximum. It is deliberately
small for illustrative purposes and to avoid the inherent complexity in the fixture feature to obscure the points on Specs-driven development, and yet it will turn out to contain at least six decisions nobody made, exemplifying how even smaller features often hide much more inside, complexity is fractal.

---

## 1. The problem is not the conversation

Simply and naively, ask a model for a promotion engine or a loyalty program and you will sure get one, derived from God knows where - which I call derivative, rather than generative, AI. Ask again for tiering and seasonal multipliers and you get those too. Nothing about that is ineherently wrong but it is not complete, or the best, or what you or your customer really wanted or needed.

The problem is that the conversation is the only place the intent lives. And conversation is imprecise, ambiguous, it has low communication temperature and it is not an artifact.

Karpathy's term for this way of working is *vibe coding*: building guided mainly
by informal exchanges, with no specification governing each change. As a way to
find out whether an idea is worth pursuing, it is excellent. As a way to run
something that has customers, it has a specific and predictable failure shape.

### The five symptoms

They are invisible while a project is small. They arrive together when it grows,
or the first time it goes to production.

**Context disperses.** The rules end up spread across chat logs, tickets, a
README, feedback by the water coooler and the code. Every new session reconstructs them from scratch, and reconstructs them slightly differently.

**Gaps get filled without agreement.** Faced with an ambiguity, a model picks
something reasonable. Reasonable is not the same as agreed, and it is not
necessarily right for this business. The model might not know better or know to ask the user, and even the user, in the heat of the moment, will not give the best and well-thought answer.

**Partial compliance goes unnoticed.** The agent solves the visible part of the request and quietly drops a secondary condition. Having asked for something in writing is not the same as having got it.

**Execution depends on the session.** A rate limit, a dropped connection or an
exhausted context window interrupts the work without making clear what finished
and where to resume.

**Functional is not well built.** Security, maintainability, auditability and
cost behaviour do not appear on their own. They need to be asked for explicitly,
and then checked.

And a sixth that is easier to miss than any of them: code can compile, run and
look right while failing to do what was intended. "Do the right thing, and do the thing right" the saying goes.

### A second way to describe the same loss

Microsoft's engineering blog frames the problem differently and the framing is
worth having, because it locates the damage somewhere more specific than "the
conversation". It calls the phenomenon **translation loss**: the loss of meaning
as an idea moves from stakeholder need to requirement, from requirement to
architecture, from architecture to implementation, and from implementation to
validation. Four handoffs, each one lossy.

The two diagnoses are compatible and they suggest different remedies, which is
why both are useful. If the problem is that intent lives only in a conversation,
the fix is an artifact. If the problem is loss at each handoff, the fix is a
single artifact that all four stages read from rather than four documents that
paraphrase each other. The second is the stronger claim and the harder one to
achieve, and it is the one that argues for keeping the specification in the
repository rather than in a wiki.

---

## 2. "It works" is not "it complies"

This distinction organises everything else, so it is worth being pedantic about.

| | **It works** | **It conforms** |
|---|---|---|
| Answers | Does the program run? | Does it match a behaviour agreed in advance? |
| Observed by | Looking at the screen | Comparing against requirements and evidence |
| Needs | Nothing written beforehand | A persistent artifact |
| Leaves | A demo | A reproducible trace |

When an agent reports "done", that sentence on its own carries almost no
information. It is a claim about the first column. Closure belongs in the second.

The operational consequence is the whole of spec-driven development in one line:
**the specification governs the change, not the other way round.** Any code
should be traceable back to it, and should pass reproducible checks before it
counts as finished.

---

## 3. Where the boundary actually is

The previous two sections argue that structure earns its keep. They do not say
when it does not, and a guide that only ever argues one way is a brochure.

### The word has drifted

Karpathy's coinage described something narrow and specific: throwaway work where
you "fully give in to the vibes" and stop looking at the code at all. Weekend
projects. Things you would delete rather than debug. Used that way it is not a
lapse in discipline, it is the correct amount of discipline for the stakes.

In common use it has widened to mean roughly "writing software with a model",
which is now most software. That drift makes the argument circular: people defend
the practice by pointing at the wide meaning and criticise it using the narrow
one, and both sides are right about different things. Everything below means the
narrow one.

The same thing is happening to the word on the other side. Böckeler reports
hearing people use "spec" as a synonym for "detailed prompt", which is a
different activity with the same name: a long prompt is consumed once and thrown
away, and nothing about writing one creates an artifact anybody can disagree
with later. If "spec" ends up meaning "prompt I took some trouble over", the
whole distinction this guide is about disappears into a style preference.

### What degrades, and in what order

The interesting claim is not that quality falls. It is that the losses arrive in a
fixed order, and that the code keeps working through all of them, so the signal
that would tell you to stop never comes.

1. **You lose why.** The behaviour is there and the reason is not. Nobody notices,
   because nobody is asking yet.
2. **You lose whether it still works.** Tests exist, and they were written to
   agree with whatever the code already did, so they cannot fail in the direction
   that matters. Green means the code has not changed, not that it is right.
3. **You lose the ability to change it.** Faced with a request, nobody can tell
   which of the current behaviours were agreed and which were accidents, so every
   change is either too timid or breaks something nobody knew was load-bearing.

Take the running example. One sentence about tripling a points balance produced
six decisions nobody made. That is one feature. Ten features in, there are sixty
of them, no record of which is which, and a system whose behaviour is the sum of
sixty coin flips that all landed while somebody was looking at the screen and
seeing it work.

The cost is not just deferred, it is transferred. Whoever gains the speed is
usually not whoever pays for it, and the bill arrives on a different desk, months
later, under time pressure. That is an accounting observation rather than a moral
one, and it is the reason the practice keeps spreading: at the moment of the
decision it is genuinely free.

### The dangerous zone is the middle

Neither pole causes much trouble. A throwaway script vibed in ten minutes is fine.
A regulated payments flow with a specification and a gate is fine. The damage
happens to the prototype that quietly stops being a prototype.

Nobody decides to promote it. It just stops getting deleted: a demo goes well, a
colleague starts relying on it, an integration points at it, and at no moment does
anyone hold a meeting about whether the thing now needs a specification. By the
time the question is obvious, the six decisions per feature are already load
bearing and undocumented, and writing them down means archaeology rather than
authorship.

If there is one operational recommendation in this guide, it is this: decide out
loud, once, that a thing has crossed over. The crossing is cheap to mark and
expensive to reconstruct.

### The test

Not how long the code will live, and not how important it is. Both are guesses
people get wrong in the optimistic direction.

> **Will anyone have to change this without having written it?**

That includes you in three months, which is a different person with the same
name. If the answer is genuinely no, vibe it and enjoy it. The moment the answer
is yes, the artifacts cost less than the archaeology, and they cost less the
earlier they exist.

### What structure costs, honestly

Spec-driven development is not free, and the case for it is weaker when the price
goes unmentioned.

- **A step before the code.** Every change starts somewhere other than the
  editor. For small changes that overhead is a real fraction of the work.
- **Artifacts that rot if unmaintained.** A specification nobody updates is worse
  than none, because it is believed for a while.
- **Tokens and time.** Templates, plans and reviews all consume both, and on a
  small change the ratio is unflattering.
- **A genuine risk of ceremony.** Process has a way of becoming its own
  justification, and once it does it consumes effort while producing documents
  rather than decisions.
- **Premature commitment.** This is the one least often admitted. When you do not
  yet know what you want, writing a specification first can make the thinking
  worse, not better: it dresses a guess as a decision and then everything
  downstream inherits it. Exploration is where vibe coding is not a compromise
  but the right tool, and pretending otherwise is how teams end up specifying
  things they should have thrown away.

### How it fails when you do it

Costs are what you pay. These are the ways the practice goes wrong while
appearing to work, and they are worth reading as a list of things to watch for
rather than as reasons not to start. Piskala's report catalogues five, and they
match what practitioners report.

**Over-specification.** The specification acquires so much detail that it becomes
pseudo-code. The test is blunt and useful: *if your spec reads like code, you have
gone too far.* You have constrained the implementation without deciding anything
extra, and lost the one property that made the document worth having.

**Specification rot.** The spec-anchored failure. Code moves, the specification
does not, and for a while people still believe it. The only reliable answer is
mechanical: something has to fail when the two diverge, which makes drift painful
instead of silent.

**Specification as bureaucracy.** The document becomes a form to fill in rather
than a tool for thinking. Once that happens people either game it or quietly stop,
and both look like compliance from a distance.

**Tooling complexity.** Teams drown in generated plans, task lists and
intermediate documents. Böckeler, working through three of these toolkits by hand,
put it plainly: *"I'd rather review code than all these markdown files."* That is
not laziness. Review capacity is finite, and a process that spends it on
artifacts has less of it left for the thing that ships.

**False confidence.** The subtlest, and the one that connects to the argument in
the next-but-one section: a passing specification test guarantees that the code
matches the spec. It says nothing about whether the spec was right. *If the spec
is wrong, the code will faithfully implement the wrong thing*, and it will do so
with a green build and a traceability matrix.

The position this guide takes is not that structure always wins. It is that the
crossing point arrives earlier than it feels like it does, that it arrives without
an announcement, and that every one of the five failures above is easier to
recover from than the archaeology you are avoiding.

---

## 4. Context, procedure and automation are not specifications

Most teams reach for three mechanisms before they reach for specifications, and
all three are worth having. None of them is a specification, and confusing them
is the most common way to feel governed while not being governed.

### The project file

A markdown file at the root of the repository acting as project memory:
conventions, structure, rules, prohibitions, the commands that matter.
`CLAUDE.md`, `AGENTS.md`, `.cursorrules`, the name varies.

It works best when it holds short, local, actionable rules. It works badly as a
store for everything, because a large one inflates context, accumulates
contradictions, and makes it unclear which artifact has authority.

*Answers:* who am I in this repository?
*Does not answer:* how the product is supposed to behave.

### Skills

A packaged way of performing a class of task: instructions, templates, examples.
The point is portability between projects. A skill is selected by meaning, so its
description is part of its design: "helps with coding" tells the agent nothing
about when to reach for it.

*Answers:* what do I know how to do anywhere?
*Does not answer:* whether the result satisfies a business rule.

### Hooks

A command the environment runs on its own when a moment arrives: after editing a
file, before a commit, at session start. Unlike a skill, a hook cannot be skipped
by the agent.

*Answers:* what happens no matter what?
*Does not answer:* whether what runs checks anything that matters. A hook can run
the tests. It cannot write them, and it cannot judge whether they test the right
thing.

### What none of the three tells you

Take the promotion. None of these files says:

- what happens when the tripled balance exceeds the cap
- how the points are calculated
- which behaviour is still in force after the change
- what was decided, and why
- what evidence demonstrates, today, that it holds

Context, procedure, specification and evidence are four different artifacts.
Mixing them makes it easier to start. Separating them is what makes it possible
to govern something that keeps changing.

---

## 5. The rule that looks simple

Here is the running example stated as loosely as a real request usually arrives.

> When a customer redeems a Triple Points token, triple their points balance,
> without exceeding the account maximum.

Every clause is clear. Together they force decisions that the sentence does not
contain.

- Does it triple the balance, or only points earned in the current period?
- What happens when the result exceeds the maximum?
- If two tokens are redeemed in the same batch, does the cap apply once or twice?
- Which balance does the multiplier read, the one before or after other pending
  accruals?
- In what order are simultaneous redemptions resolved?
- Does replaying the same batch produce the same final balance?

A model asked to implement this will answer all six. It has to, in order to emit
code. It will answer them silently, reasonably, and without telling you which
answers were yours and which were its own.

That is the gap specifications fill. Not "documentation". The distinction between
what was asked for and what was assumed.

### Making the model say what it does not know

The most direct mechanism for this comes from GitHub's Spec Kit, and it is almost
embarrassingly simple. The specification template instructs the model to write
`[NEEDS CLARIFICATION: the specific question]` wherever the request does not
determine an answer, and forbids it from filling the gap: *"Don't guess. If the
prompt doesn't specify something, mark it."*

It works because it inverts an incentive. A model asked for a specification will
otherwise produce a complete-looking one, because completeness is what
specifications look like, and a document with no holes in it reads as finished
work. Told to mark the gaps instead, it produces a document whose holes are the
useful part: those six questions above, in writing, before anyone has committed
to an answer.

The limit is worth stating, because this is easy to adopt and easy to render
decorative. A marker helps only if something refuses to proceed while one
remains. Spec Kit puts *"no [NEEDS CLARIFICATION] markers remain"* in a
checklist, and a checklist is a reminder. If your process treats a marked
specification as ready to build from, you have added a syntax for recording
uncertainty rather than a mechanism for resolving it.

### The stable rules, once someone decides

| ID | Rule |
|---|---|
| FR-001 | Redeeming a Triple Points token sets the balance to `min(3 × n, MAX_BALANCE)` |
| FR-002 | `MAX_BALANCE` is never exceeded |
| FR-003 | Each token is consumed once, even within a single batch |
| FR-004 | The same batch and starting balance produce the same final balance |
| FR-005 | The cap is applied after all accruals in the batch, not before |
| ADR-001 | Simultaneous redemptions are ordered by `(timestamp, account_id, token_id)` so results are reproducible |

Six rules and one recorded decision, from one sentence. That ratio is normal, and
it is the argument for writing them down rather than discovering them in
production.

---

## 6. This did not start with AI

Worth knowing, because it changes how you read the current tooling. Almost none
of the ideas are new. What is new is the reason they suddenly matter.

**2004.** "Specification-Driven Development" appears in academic work by Ostroff
and colleagues, combining test-driven development with design by contract. The
motivation was the same then as now: tests show that specific cases pass;
contracts state what should hold in general.

**2009.** EARS, Easy Approach to Requirements Syntax, comes out of work at
Rolls-Royce. It is a small set of sentence patterns that constrain how a
requirement may be phrased, in order to reduce ambiguity. Not eliminate it,
reduce it. That modesty is characteristic of the good work in this area.

**2021.** An internal API standard I wrote as architecture lead at a
multinational states the position without any of the current vocabulary:

> Be API-First. Define your API properly before start implementation. The API
> first principle is an extension of contract-first principle. Therefore,
> development of an API MUST always start with API design without any upfront
> coding activities. **The design of the API is the source of truth, not the
> implementation.** The contract represents the agreement between API
> stakeholder, implementers, and consumers.

That is spec-anchored development, mandated in a corporate standard, four years
before anybody was calling it spec-driven development. It is in the timeline for
two reasons. The first is that a claim about how old these ideas are is stronger
with a dated primary source than with a borrowed citation. The second is more
useful: the standard was adopted, and what made it adoptable had nothing to do
with the idea. It had a document number, a revision history, named owners, a
compliance section and a route for exceptions. The idea was the easy part.

**2025.** Sean Grove's "The New Code" argues that specifications, not code, are
the artifact worth investing in when generation is cheap.

**2025.** Birgitta Böckeler, writing on Martin Fowler's site, separates the
current practice into three positions rather than one: spec-first, spec-anchored
and spec-as-source. That distinction is the most useful thing in the current
literature and section 7 is built on it.

**2026.** Preprints and tools proliferate. Treat them as signals, not consensus.

The pattern across the whole timeline is worth naming, because it predicts what
happens next. Each of these arrived as a local answer to a local problem:
contracts for a verification community, sentence patterns for aerospace
requirements, API-first for teams whose integrations kept breaking. None of them
arrived as a methodology, and the two that became methodologies, model-driven
development and to an extent agile, are the two that people now describe as
having failed. That is not a coincidence, and it is the strongest argument for
adopting the mechanisms in this guide one at a time, against a problem you can
name, rather than as a programme.

Underneath, spec-driven development is a bundle of older practices answering
three questions:

| Question | Practices |
|---|---|
| What should the system do? | Requirements, user stories, EARS, examples |
| How will we know it does? | TDD, BDD, contracts, property-based testing |
| Why was it built this way? | Architecture decision records |

In a workflow with agents this vocabulary acquires a second job. It becomes a
containment system: it bounds what the agent is allowed to decide on its own.

---

### The precedent worth being nervous about

One historical parallel is sharper than the rest, and it is a warning rather than
a reassurance. Model-driven development, in the 2000s, tried exactly this: formal
models as the primary artifact, code generated from them. Böckeler, who worked on
it early in her career, gives the post-mortem in one line. It failed because it
occupied *"an awkward abstraction level and just creates too much overhead and
constraints."*

The optimistic reading is that large language models remove precisely what killed
it: you no longer need a rigid parseable syntax, or a generator somebody has to
maintain, and natural language sits at whatever abstraction level you like. That
is true, and it is why the idea is back.

The pessimistic reading is the one worth keeping in view. What model-driven
development also had was tool support: a model was checkable for validity,
completeness and internal consistency by a program, because it had to be. Natural
language specifications have none of that. Böckeler's warning is that spec-as-source
could arrive with *"the downsides of both MDD and LLMs: inflexibility and
non-determinism"*, which would be a genuinely new low: the rigidity of generated
code plus the unpredictability of the thing generating it.

That is not a prediction. It is the failure mode to check for, and the reason the
preconditions in the next section are written as preconditions rather than as
advice.

---

## 7. The spectrum: who edits what

This is not a maturity model and you do not have to climb it. It is a way of
asking one question about your own project: **if the specification and the code
disagree, which one is wrong?**

### spec-first

The specification is written first, in order to think more clearly. Once code
exists, the code is what gets edited.

- **On conflict:** the maintained code wins.
- **How drift shows up:** the spec silently ages.
- **Honest use:** thinking tool, design review, onboarding.

Most teams that say they do spec-driven development are here. There is nothing
wrong with it as long as nobody pretends the document is normative.

### spec-anchored

The specification stays normative. A change begins there, and code is then
modified or regenerated to match.

- **On conflict:** the ratified spec wins, and the code is corrected.
- **How drift shows up:** comparison, review and tests catch it.
- **Cost:** every change has a step before the code.

### spec-as-source

Nobody edits the generated output. Changing the system means changing the
specification and rebuilding.

- **On conflict:** the spec and the generation process win.
- **How drift shows up:** rebuild, plus detection of manual edits.
- **Precondition:** repeatable regeneration, manual-edit detection, and CI that
  protects behaviour. Without all three this is aspiration, not a position.

The sensible default is to start spec-anchored and move a single module to
spec-as-source only once those three preconditions are genuinely in place. Moving
the whole system at once is how teams end up editing generated files in secret.

### The rule for choosing

Piskala's report states the choice more crisply than anything else I have read on
it, and it is the sentence to remember if nothing else here survives:

> **Use the minimum level of specification rigor that removes ambiguity for your
> context.**

Minimum, and for your context. Spec-first while a model is doing the initial
build and the ambiguity is mostly in your own head. Spec-anchored for anything
long-lived enough that somebody else will maintain it. Spec-as-source only where
the generation tooling is mature and trusted, which for most teams and most of
this decade means not yet.

Worth noting that this taxonomy now arrives from two independent directions:
Böckeler defined the three levels from hands-on work with the tools, and Piskala
reaches the same three from a survey of practice. Two sources converging on a
distinction is weak evidence that the distinction is real, which is more than most
vocabulary in this field has.

### The claim that there is no gap

Spec Kit's manifesto states the maximalist version of spec-as-source, and it is
worth quoting because it is the position this guide is arguing with. The gap
between specification and implementation, it says, *"has plagued software
development since its inception"*, and previous approaches only tried to narrow
it. Now: *"When specifications and implementation plans generate code, there is no
gap, only transformation."*

The first half of that is true. The second half moves the gap rather than closing
it.

What disappears, when generation is genuinely repeatable, is the distance between
the specification and the code. What remains undiminished is the distance between
the specification and what anyone actually wanted. Every one of the six questions
in the previous section can be answered wrongly in a specification, generated
faithfully into code, and pass every test derived from that same specification.
Internal consistency is not correctness. A system that regenerates cleanly from a
wrong specification is a system that is wrong faster and more thoroughly than
before.

This is not an argument against the position, and the position is not a
marketing claim: it follows from taking generation seriously. It is an argument
about which problem the position solves. Spec-as-source removes drift, which is a
real and expensive problem. It does not remove the need for somebody to be right,
and it concentrates the whole cost of being wrong into a single artifact that now
has nothing downstream to disagree with it.

Which is the reason the rest of this guide is about ratification and gates rather
than about generation. The better the generation, the more the remaining risk sits
in the one place nobody is checking.

---

## 8. The gate

A gate is not a check. A gate is:

> **executable check + mandatory policy + effective block**

Take those three apart, because most "we have CI" claims fail on one of them.

**Executable.** A machine runs it and produces a reproducible verdict, not an
opinion. A model reviewing its own diff and reporting "looks correct" is not
executable, however useful the review is.

**Mandatory.** It is wired into integration and cannot be bypassed. A check that
exists but is not required is a suggestion.

**Blocking.** Red stops the change. Red that merely warns is a notification.

Installing a validator does not create a gate. A green run on a laptop does not
protect the main branch.

### The ratchet

The useful mental image is a ratchet: it lets the load move forward and does not
let it slip back on its own.

A test becomes a tooth on that ratchet when four things are true:

1. It expresses a rule a person has ratified.
2. It is versioned.
3. Whoever implements the change cannot alter the expected result without a
   separate review.
4. It runs as a required check before integration.

Point 3 is the one that gets skipped, and it is the one that matters. If the same
agent can write the implementation and relax the test, there is no ratchet, only
a ritual.

The ratchet protects what the team managed to express. Not everything it wanted.
And it does not prevent change: if the promotion multiplier should become four
rather than three, you open a change, edit the spec, ratify the new expectation,
and close the gate behind it.

### Gates that constrain the shape, not only the compliance

Everything above is about verifying a change after it exists. There is a second
kind of gate, aimed at a failure mode that verification cannot catch and that is
specific to working with models: the answer is correct and four times larger than
the question.

Spec Kit runs three checks before implementation begins:

- **Simplicity.** Three projects or fewer? Is anything here future-proofing?
- **Anti-abstraction.** Is the framework used directly, or wrapped? One
  representation of each model, or a parallel one alongside it?
- **Integration-first.** Are the contracts defined? Are contract tests written
  before the implementation they describe?

No test fails when these are violated. A model asked for a points promotion will
produce an interface, a factory, an abstraction over the database and a service
layer, all of it working, all of it passing, all of it reviewed by someone who is
reading for correctness because that is what review is for. Nothing about the
result is wrong except its size, and size is the property nobody is assigned to
check.

The part worth copying is not the three questions. Those are opinions, and yours
may reasonably differ. It is the escape valve. A gate you cannot fail is theatre;
a gate with no exceptions is bypassed within a month. Spec Kit permits the
violation and requires it to be written down, in a section it calls **complexity
tracking**: whoever wants the fourth project explains why, in the artifact, where
the next person will find it. That turns a prohibition into a record, which is the
same trade the ratchet makes, and the reason both survive contact with real work.

### The separation that makes this work

| Responsibility | Where it lives | Contains |
|---|---|---|
| Authority | Ratified specs and decision records | Human judgement |
| Reproducible checking | Build, schema validation, static analysis, tests with controlled seeds | No judgement at all |
| Enforcement | CI, branch protection, permissions | Policy, mechanically applied |

The single most important property of this arrangement: **no mechanism authorises
the model to ratify its own output.** The agent proposes, a person ratifies, a
program checks. Collapse any two of those into one and the guarantees go with it.

The objection to this is common enough to be worth answering, and it turns up in
the comments under the Microsoft article in almost pure form: agents are good
enough now that human checkpoints are ceremony. The answer given there is the best
short one I have seen, and it is a distinction rather than a defence.
**Implementation autonomy** is how much of the work the agent does without being
asked, and it should rise as the tooling improves; there is no virtue in typing
code a model would type better. **Decision autonomy** is who is answerable for
the outcome, and it does not transfer, because it cannot: an agent cannot be
accountable, and a team that behaves as though it can has not delegated
responsibility, it has mislaid it.

Which is why the gate is not a comment on how capable the model is. Raise
implementation autonomy as far as your tooling will carry it. The gate exists
because somebody still has to answer for the result.

---

## 9. The adjacent layers

Spec-driven development is usually met alongside three or four other names, and
it is worth being clear about how they relate, because they are routinely
presented as rivals and they are not. They operate at different layers, and the
question each one answers is different.

| Layer of concern | Unit | Question it answers | Where state lives |
|---|---|---|---|
| Inference | The single call | What shape does this invocation have? | In the request and the decoding |
| Context | The window | What does the model see, and what gets evicted? | In the context |
| Loop | The control flow | When do we stop, retry or escalate? | In the harness |
| The Ralph loop | The iteration | Can the outer loop be dumb if the filesystem is smart? | On disk |
| Specification | The change | Who decides, and what demonstrates it? | In ratified artifacts |

Four of those five are about making the machine work better. Only the last one is
about who decides. That difference in kind is why specification work does not
compete with the others and can borrow from all of them.

### Each layer has a failure mode the layer above cannot see

This is the practical reason to care about all of them rather than picking one.

**Inference done well** gives you a structurally valid response that is
semantically wrong. A schema knows nothing about your business.

**Context done well** gives you a thoroughly informed agent that is confidently
wrong about a rule nobody wrote down.

**Loop done well** gives you convergence. Convergence towards something nobody
agreed to.

**A Ralph loop done well** leaves a repository full of accumulated decisions and
none of them ratified. It is the most effective of the four at producing code,
which is exactly why it accumulates unexamined intent fastest.

**And specification work without the other four** gives you a beautiful document
that is expensive to execute.

### What specification work should take from each

**From inference engineering**, two things, and the first is the cheapest
improvement available anywhere in this stack. Constrained or schema-guided
decoding turns a validated contract into an unexpressable one. If the proposal
step requires the model to return an object conforming to a schema, validating
the response and rejecting bad ones is good; making the bad ones impossible to
emit is better. Moving a check from *rejected* to *cannot be said* removes a whole
class of retry.

The second is cost. A spec-anchored flow re-sends the same ratified specification
on every call, and providers bill cached prefixes at a fraction of the normal
rate. Put the invariant sections first and the variable ones last and most of that
context is nearly free. Specification literature is generally silent about cost,
which is a gap, because "this is slower and dearer" is the first objection anyone
raises.

**From context engineering**, the practice of just-in-time retrieval rather than
pre-loading. The instinct when specifications become normative is to hand the
agent the whole specification. Context engineering says hand it the identifiers
and let it fetch what it needs, which is precisely what a repository organised
around IDs and typed relations makes possible.

There is also a convergence worth naming. Context engineering arrived at "move
state out of the window and into files" because the window is scarce.
Specification work arrives at the same place because the window is not
authoritative. Same practice, two independent reasons, which is usually a sign
the practice is right.

And sub-agent isolation, which appears in specification tooling as roles with
different write permissions, is justified twice over: context engineering wants it
for context hygiene, specification work wants it for separation of duties.

**From loop engineering**, budgets and turn limits, and one pattern that deserves
to be stolen more aggressively than it is: *a retry is only granted when the input
contains a new hypothesis*. If a failure reproduces the same signature with no
identifiable change, that is not progress and should not be presented as
progress. This single rule is the difference between a loop that converges and a
loop that spends money.

**From the Ralph loop**, the idea that most usefully puts pressure on everything
above. Ralph is a deliberately unintelligent outer loop: re-run the agent against
the same instructions, and let it re-read the state from the filesystem each time.
Because the state is on disk rather than in the harness, the loop survives context
exhaustion, a crash, and a lost session.

A phase machine of the kind described in section 14 is a *clever* loop, and clever
loops hold state. The Ralph reading suggests the phases should be reconstructible
from disk rather than held in an orchestrator's memory, and that a local
checkpoint is not a durable execution. That is a real design constraint, not a
stylistic preference.

Ralph also supplies the variable that determines whether any of this works: task
granularity. An obligation sized so that no single iteration can close it is an
obligation that will sit at `pending` forever, and it will look like an agent
problem when it is a decomposition problem.

### One mechanism, two names

If you have written about Ralph loops you will already have met *backpressure*:
the tests, type checks and linters that push back on the loop and stop it running
away. Backpressure and the gate from section 8 are the same mechanism named from
opposite ends. The loop view names what pushes back; the specification view names
the three properties that make the push effective, and adds the asymmetry the loop
view leaves implicit: whoever implements the change must not be able to weaken the
oracle.

### A note on the names themselves

Treat this table as layers of concern rather than as five established
disciplines. "Context engineering" is a consolidated term. "Loop engineering" and
"inference engineering" are not, at least not to the same degree, and the latter
is used in two different senses: the infrastructure of serving models, meaning
batching, cache management and quantisation, and the shape of an individual
invocation, meaning constrained decoding, sampling and retry policy. Only the
second is relevant here.

Presenting all five as named fields would overclaim. Presenting them as layers,
each with a unit of concern and a characteristic blind spot, is defensible and
more useful.

The reason this section comes before the tools is that it explains what to expect
of them. Most tooling in this space is strong at one or two layers and silent
about the rest, and no product covers the layer where authority lives, because
authority is not a feature.

---

## 10. The template is a prompt

This is the idea in the current tooling that transfers best, and it is easy to
miss because it arrives looking like paperwork.

When Spec Kit ships a specification template, the template is not a form for a
person to fill in. It is an instruction set aimed at the model that will fill it
in, and its clauses are written to counteract specific things models reliably do.

| The clause | The behaviour it counteracts |
|---|---|
| Focus on what users need and why. Avoid how to implement: no tech stack, no APIs, no code structure | A model asked for requirements is choosing a database by the second paragraph |
| Mark all ambiguities. Do not guess | Filling gaps with the most plausible answer, silently |
| A completeness checklist at the end of the document | Producing something complete-looking and never re-reading it |
| Create contracts first, then tests, then source | Writing the implementation and then tests that agree with whatever it did |
| No speculative or "might need" features | Building for the requirement it imagines you will have next |
| Code samples and long algorithms go in a separate details file | A specification that degenerates into an unreadable code dump |

Read as documentation, that is a style guide. Read as what it is, it is a set of
constraints applied at the moment of authorship instead of at review, which is
the only moment at which they are cheap.

The generalisation, and the reason this belongs in a guide rather than in a tool
comparison: **the artifacts of a spec-driven process are the prompt.** Their
headings decide what gets thought about. Their order decides what gets thought
about first. Their explicit prohibitions are the only part of the whole process
that operates before a mistake exists rather than after it. A team that writes its
own templates is writing its own model behaviour, whether or not it thinks of the
work that way.

### What happened when somebody tried it

All of which is the theory. Böckeler worked through three of these toolkits by
hand and found the mechanism holds much less firmly than its design implies.
Agents ignored the templates. In one run, Spec Kit's own research step correctly
identified the classes that already existed, and the agent then generated new ones
alongside them, producing duplicates the research had been added to prevent. In
others they went the other way and *"way overboard because it was too eagerly
following instructions."*

So the template is a prompt, and a prompt is a request. That is the honest version
of this section. Templates raise the probability of the behaviour you want; they do
not produce it, and a larger context window does not mean the model has read what
is in it. Böckeler's name for the resulting feeling is worth borrowing: a
checklist-heavy workflow can create *the appearance of rigour without delivering
any*, and appearance is more dangerous than absence because it stops people
looking.

That does not make templates worthless. It makes them the cheap half of a pair.
Everything they merely request, a gate has to require, and anything you cannot
express as a gate remains a hope however emphatically the template phrases it.
She has a word for the whole class of intervention that makes things worse by
trying to improve them, and it deserves to survive the translation:
*Verschlimmbesserung*.

### The strongest version of the idea, and what it smuggles in

Spec Kit's most distinctive artifact takes this further than a template. It calls
it a **constitution**: a file of numbered articles that every specification and
plan gets checked against. Some of them are strong claims about how software
should be built, and they are worth naming, because installing the tool adopts
them.

Every feature begins life as a standalone library. Every library exposes a
command-line interface taking text in and text out. Tests are written and
confirmed failing before any implementation exists, which the document calls
non-negotiable. Three projects maximum without written justification. Use
frameworks directly rather than wrapping them. Real databases in integration tests
rather than mocks.

Read that list again as what it is: a set of architectural opinions, held by one
organisation, arriving in your repository as configuration. Several are defensible
and a couple are contentious, and the point is not which. It is that a project
adopting the tool inherits all of them and will enforce them on every feature
afterwards, whether or not anybody read the file.

The design decision worth stealing regardless is that several articles are left
deliberately blank, for the project to fill with its own non-negotiables. A
constitution that arrives fully written is somebody else's constitution.

So: read the ones you adopt. The three gates in the section before this one and
the articles above are not neutral scaffolding. They encode a specific view about
project structure, abstraction and testing, and the parts that are wrong for you
will otherwise be enforced silently for as long as nobody notices.

---

## 11. How legal requirements are served by this

Legal and ethical constraints are the most neglected class of requirement in
software, and the one this machinery happens to fit best. Both halves of that are
worth arguing.

Nothing here is legal advice, and the distinction matters more than the
disclaimer usually does: everything below is about *where a decision gets made
and who answers for it*, which is an engineering question. What the rule should
be is not, and the whole point of the arrangement is to stop engineers answering
it by accident.

### The one requirement that arrives pre-specified

Most requirements have to be extracted from somebody who has not finished
thinking. Legal ones arrive already written down, by somebody else, and are not
negotiable. That should make them the easiest input this process ever gets.

They are not, because they arrive at the wrong altitude. "Personal data shall be
adequate, relevant and limited to what is necessary" is a principle, and a
principle is not something a test can fail. The work is the descent: from a
principle nobody disputes, to a rule about this system, to a check that runs.

For the running example, a promotion engine reading customer balances:

| Level | Statement |
|---|---|
| Principle | Collect no more than the purpose requires |
| Rule for this system | The promotion evaluator receives account id and balance, and no other customer attribute |
| Check | A contract test on the evaluator's input, failing if the payload gains a field |

Only the third row survives contact with a codebase, and only the first row is
what anybody in a compliance conversation will say to you. Everything useful
happens on the middle row, and that row is the one nobody writes down.

### Where the fit is unusually good

Regulated work needs three things that are otherwise a separate and resented
exercise: a statement of intended behaviour, evidence that the system does that,
and a record of who decided. Those are the specification, the gate and the
decision record. A team already working this way produces compliance evidence as
a byproduct rather than as a project.

That is the strongest practical argument in this guide, and it is worth stating
carefully, because the inverse is what usually happens. Compliance evidence
assembled after the fact is archaeology performed under deadline by whoever is
available, and its quality reflects that. The same evidence falling out of a
process that was going to run anyway costs approximately nothing.

### The decisions that carry legal weight and get made silently

These are the ones that show up in code review as ordinary technical choices, and
in an incident as something else. The pattern is the same as the six questions in
section 5: nobody refuses to decide, somebody decides quietly.

- **Retention.** A duration is a design decision with a legal consequence, and it
  is usually a configuration default that somebody typed once.
- **Logs.** The most reliably forgotten one. Logs are personal data, they are
  copied to more places than the database, they are retained longer, and they are
  read by more people.
- **Lawful basis.** Not a paragraph in a policy. It maps to a code path, and the
  question "which basis is this branch operating under" has an answer whether or
  not anyone has written it.
- **Cross-border transfer.** Chosen by a deployment region, in a Terraform file,
  by whoever set up the environment.
- **Deletion.** A distributed systems problem wearing a compliance hat. Caches,
  replicas, backups, search indexes, the analytics warehouse, and the logs above.
- **Telemetry defaults.** Where the law's floor and a product's interest diverge
  most visibly, decided by a boolean's default value.

None of those needs a lawyer to *decide*. All of them need somebody to notice a
decision is being made, and to route the ones that matter to whoever can ratify
them. That is the entire mechanism: legal ratifies the rule, engineering ratifies
the mechanism that enforces it, and the decision record holds the conversation so
the next person does not reopen it from zero.

The failure mode has a name and it is worth being blunt about it: **the developer
decided.** Not maliciously and usually not even consciously. It is the same
failure as the promotion cap, with an external consequence attached.

### What is genuinely new

One thing here is not an old problem in new clothes.

A model writing code makes these decisions at a rate no review process was built
for, and it makes them the way it makes all the others: reasonably, plausibly,
and without saying so. A retention default, a log line containing an email
address, a field added to a payload because it was available. Each is individually
defensible and none of them was ratified.

And a genuinely new category, which is the one to think about hardest: **what
leaves the building in a prompt.** Sending a customer record to a model provider
is a data transfer to a third party, and it is initiated by a line of application
code that looks like a function call. The provider is a processor. The content of
the context window is disclosed data. Almost none of the tooling in this area
treats it that way, and almost none of the existing compliance vocabulary was
written with it in mind.

The corresponding specification work is unglamorous and small: state what may
appear in a prompt, as a rule, and make it checkable. A test asserting that the
payload assembled for a model contains no field from a denylist is a crude
instrument. It is also the difference between a policy and a control.

### Where the law stops

The law is a floor. The decisions that are interesting are the ones that are
lawful and still wrong, and they are decided by the same defaults.

Consent that is technically obtained and practically unreadable. A retention
period set to the maximum the law allows because the maximum was easiest. An
inference the system is permitted to draw and that the person would object to
being drawn. A dark pattern that survives review because no rule prohibits it.

There is no gate for this, and pretending otherwise is worse than admitting it.
What the machinery does offer is smaller and real: it makes the decision visible
and attributable. A retention period sitting in a specification, with a name
against it, is a decision somebody can be asked about. The same value as an
untracked default is nobody's.

Which is the honest summary of this whole section. Spec-driven development does
not make a system lawful or ethical. It makes the decisions that determine
whether it is into things that exist, have owners, and can be questioned before
rather than after.

---

## 12. One repository, four representations

If specifications are going to be normative, they need somewhere to live that is
not a wiki. The arrangement that holds up is plain files in the same repository
as the code, with each thing in exactly one place.

| Representation | Question | Holds |
|---|---|---|
| Intent | Why do we want to change? | The literal request, unsummarised |
| Specification | What should happen? | The ratified rules in force, and proposals in isolation |
| Evidence | What is checked? | Acceptance cases, contracts, tests |
| Implementation | What happens today? | Source, and the record of what ran |

These are not four levels of truth ranked by authority. They are four
representations of the same project, each answering a different question. What
makes them a system rather than four folders is that identifiers let you walk the
chain:

```
INT-001 → CHG-001 → FR-001 → CP-014 → TEST-001 → src/promotions.js → RUN-042
```

Being able to walk that chain in both directions is the whole point. Forwards it
answers "is this implemented and checked?". Backwards it answers the question
that actually gets asked in incidents: "why does it do this, and who agreed?"

### Two layers in one file

The convention that makes this work with ordinary tools is frontmatter for
machines, body for people.

```markdown
---
schema_version: 1
type: requirement
id: FR-001
status: ratified
capability: promotions
relations:
  derives_from: [INT-002]
  decided_by: [ADR-001]
  verified_by: [TEST-001, PBT-002]
---

# Triple Points token

## FR-001 - Balance multiplication

WHEN a Triple Points token is redeemed, THE SYSTEM SHALL set the
balance to min(3 × n, MAX_BALANCE).

### Examples
- 2,000 points becomes 6,000
- 40,000 points with a 50,000 cap becomes 50,000
```

The same file serves four consumers: a person reading the body, an agent
assembling context from the relations, a validator checking that the cited IDs
exist, and Git keeping the rule together with its status and its history.

The test of whether you have built this properly: **if you uninstall the note-taking
app, does everything still work?** The artifacts should be readable as plain
markdown, validatable by a script, versionable with Git and checkable in CI. If
they are not, you have built a personal wiki with extra steps.

---

## 13. When artifacts disagree

They will. The rule is that no artifact wins because of its format. The ratified
decision in force wins.

| Situation | Response |
|---|---|
| Code violates a ratified spec | Correct the code. The agreed norm is the reference |
| A test contradicts the spec | Distrust the test first: it may be protecting a wrong expectation |
| Behaviour reveals the intent was wrong | Open a change and discuss it in the open, do not patch quietly |
| The requirement itself should change | A person ratifies the new norm first, then the evidence is adjusted |

A worked example. Someone lowers the cap in the code from 50,000 to 25,000 and
touches nothing else. The test expecting 50,000 fails.

That failure settles nothing. It reports that two layers stopped agreeing.

- If nobody ratified a new cap, the norm in force is still FR-002, and the code
  is what gets corrected.
- If the business does want 25,000, the problem is upstream: open a change,
  ratify the new FR-002, and only then update the test and the code.

Note what this does *not* require. It does not require a human to physically type
every file. An agent can draft proposals, write requirements, and propose tests.
What stays human is ratifying meaning. What stays mechanical is checking.

---

## 14. The loop

Putting it together, a change moves through phases. These are internal states,
not eleven screens.

| Phase | Person | System | Agent |
|---|---|---|---|
| Capture | States the problem | Stores the literal request, opens a change | Not yet involved |
| Propose | Corrects misreadings | Assembles current state and policy | Drafts requirements and questions |
| Cover | Checks nothing is missing | Turns requirements into matrix rows | Proposes decomposition |
| Clarify | Answers blocking questions | Validates schema, IDs, relations | Finds ambiguities and contradictions |
| Ratify | Approves scope and meaning | Records who, when, and which hashes | May explain, cannot approve |
| Evidence | Approves the expected result | Protects the approved expectations | Proposes cases and properties |
| Confirm red | Decides if a surprise changes the reading | Runs the new evidence before any code | Helps interpret the failure |
| Implement | Authorises the start | Sets permissions, budget, checkpoint | Writes only in permitted paths |
| Verify | Resolves real failures | Runs validators, build, tests | Fixes, in a separate session from review |
| Integrate | Approves the merge | Checks CI and approvals on the same commit | Summarises, does not merge |
| Archive | Reads the closure | Publishes the new state in force | No longer involved |

Three things in that table do more work than the rest.

**Confirm red.** Run the new evidence *before* the implementation exists, and
require it to fail. If it passes, stop: either the behaviour already existed, or
the test does not observe what it claims, or the spec describes the current
system incorrectly. All three are worth knowing before writing code.

**The coverage matrix.** One row per obligation, carried from proposal to
closure. A row starts `pending`, which is not an error, it means the obligation
has an identity and no evidence yet. The value is that a small request containing
six obligations cannot quietly become four. The matrix is not replaced at the end
by a summary written to justify whatever shipped.

**Calculated closure.** Nobody declares the change done. Closure is computed:

```
closed = every required row verified
       AND no row pending or blocked
       AND CI green on this exact commit
       AND the ratified hashes still current
       AND the required approvals present
```

Note that the agent reports what it *believes* it addressed, and that claim never
sets a row to verified. The distinction between a claim and a verdict is the
thing being engineered.

---

## 15. What to take away

If you remember five things.

1. **The conversation cannot be the only place the intent lives.** Anything that
   must outlive a session has to be a file in the repository.

2. **Context, procedure, specification and evidence are four artifacts.** Project
   files, skills and hooks improve the agent. None of them is a specification.

3. **"It works" is not "it conforms."** Closure is measured against requirements
   and evidence, never against an assertion.

4. **A gate is an executable check plus a mandatory policy plus an effective
   block.** Two out of three is a notification.

5. **The agent proposes, a person ratifies, a program checks.** No mechanism
   authorises a model to ratify its own output.

And one thing to be suspicious of, including in this guide: none of this is
demonstrated. Structure is cheap to add and its benefits are mostly costs
avoided, which are invisible unless you measure them. If a team adds traceability
and its defect rate and cycle time both get worse, the traceability has not
earned its place. Worth measuring before believing.

---

## Sources

Listed to be checked, not to decorate. Every claim of provenance in section 6
should be verified against the original before this guide is published anywhere.

- Roberto Canales Mora, *Desarrollo de Software Basado en Especificaciones: del
  vibe coding a un sistema verificable*, preliminary edition, August 2026. The
  structural spine of this guide, and the source of the gate, ratchet, coverage
  matrix and calculated closure formulations.
- J. S. Ostroff et al., work on specification-driven development combining
  test-driven development and design by contract, 2004.
- EARS, Easy Approach to Requirements Syntax, originating in work at
  Rolls-Royce, 2009.
- Sean Grove, "The New Code", 2025.
- Birgitta Böckeler, the *Exploring Gen AI* series on martinfowler.com, 2025 to
  2026, including the instalment on the tools. The source of the three-level
  spectrum, the model-driven development parallel, the observation that agents
  ignore the templates, and *Verschlimmbesserung*. The most sceptical source here
  and the one that did the most hands-on work, which is not a coincidence.
- Deepak Babu Piskala, *Spec-Driven Development: From Code to Contract in the Age
  of AI Coding Assistants*, arXiv 2602.00180, February 2026. Read in full. A
  technical report and a synthesis of practice, with a decision framework, five
  named pitfalls and the "minimum rigor" rule. Worth being precise about what it
  is not: a single-author report with no experiment, no dataset and no
  measurement, so it is a well-organised argument rather than evidence, and
  citing it as research would be a category error. It also, incidentally,
  attributes the martinfowler.com article to Fowler rather than to Böckeler and
  adopts her taxonomy without naming her, which is this guide's own warning about
  inherited citations happening in front of us.
- Microsoft, *Spec-driven development and AI-native engineering*, developer blog,
  2026. The source of "translation loss" and of the decision versus
  implementation autonomy distinction. A vendor post: its three case studies
  quote outcomes such as brownfield onboarding falling from two or three weeks to
  a few days, with nothing published that would let anyone check them.
- Andrej Karpathy, on vibe coding, 2025.
- GitHub, *Spec Kit* and its manifesto `spec-driven.md`, 2025 to 2026. Read in
  full; the source of the constitution, the pre-implementation gates, the
  clarification markers, the templates-as-constraints idea, and the "power
  inversion" thesis this guide argues with in section 7.

---

## Open questions for the next revision

- Verify every citation above. Inherited citations are how errors propagate, and
  the Piskala entry now contains a worked example of it.
- Carlos Azaustre has a Spanish-language piece on spec-driven development with
  agents that belongs here; his site returned 403 to an automated fetch, so it
  needs reading by hand before it can be cited or disagreed with.
- The guide now has three sources arguing for the practice and one arguing with
  it. That ratio flatters the practice. Find the best available argument that
  this is a fashion, and answer it or concede it.
- The tool comparison is gone, as of this revision. It was the section that
  would age fastest, Böckeler's hands-on findings had already started
  contradicting parts of it, and a guide that ages badly in one section gets
  distrusted in all of them. What was worth keeping from it, the constitution as
  an example of a tool arriving with opinions, moved into section 10.
- The legal chapter needs a reader who does this for a living to disagree with
  it. It is written from the engineering side of a conversation that has two
  sides.
- Add one worked example end to end, in full, rather than in fragments.
- Consider a short section on cost: structure is not free, and the honest case
  for it has to include the token and time overhead. Spec Kit's own comparison,
  roughly twelve hours of documentation work against fifteen minutes of
  commands, is the claim that section would have to engage with. It is not
  obviously wrong and it is not measuring the same thing on both sides: the
  fifteen minutes buys artifacts nobody has read yet.
- The constitution idea deserves more than a paragraph inside a tool entry. If a
  project's non-negotiables belong in a file, the questions are who ratifies a
  change to it, and what makes it different from a style guide nobody follows.
