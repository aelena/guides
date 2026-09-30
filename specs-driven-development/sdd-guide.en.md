# Spec-Driven Development

### A short guide to governing change when a model writes the code

**Version 0.5 · Draft · September 2026**

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

Simply and naively, ask a model for a promotion engine or a loyalty program and you will surely get one, derived from God knows where - which I call derivative, rather than generative, AI. Ask again for tiering and seasonal multipliers and you get those too. Nothing about that is inherently wrong but it is not complete, or the best, or what you or your customer really wanted or needed.

The problem is that the conversation is the only place the intent lives. And conversation is imprecise, ambiguous, it has low communication temperature and it is not an artifact.

Karpathy's term for this way of working is *vibe coding*: building guided mainly
by informal exchanges, with no specification governing each change. As a way to
find out whether an idea is worth pursuing, it is excellent. As a way to run
something that has customers, it has a specific and predictable failure shape.

### The five symptoms

They are invisible while a project is small. They arrive together when it grows,
or the first time it goes to production.

**Context disperses.** The rules end up spread across chat logs, tickets, a
README, feedback by the water cooler and the code. Every new session reconstructs them from scratch, and reconstructs them slightly differently.

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

Two details from practice help the marker be a mechanism rather than a syntax.
The first is Fontoura's: the state that unlocks the next phase lives in a
separate one-line file that only a person writes, and the rule is flat: *file
existence does not imply approval*. A design document on disk is not a green
light; only the state token is. With that in place, an unresolved marker stops
being a note and becomes the reason the token does not change. The second is
cheaper still: before any code, ask the model to restate the rules in its own
words. If it has misread FR-002, you find out now, at zero cost, rather than
three sessions later.

And one fact about how little is known here. SpecMine, Carnegie Mellon's census
of 470,795 specification files on GitHub, counts clarification markers and
unfilled placeholders as features of every document. It is the first time
anyone can measure how many markers get resolved before code exists and how
many just sit there. Nobody has published that number yet.

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

**2026.** The first measurements arrive, pointing in two directions. A census of
GitHub counts 470,795 specification files across 73,030 repositories, 99.7% of
them created since 2025: the practice is a year old. And a study of 100,247
pull requests finds none of the benefits the vendors advertise. Section 19 is
about both.

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

Alenezi, in the most formal reference model published on this, describes the
same boundary in a different vocabulary, and it is worth having because it
makes explicit a claim that section 2 leaves implicit. In vibe coding,
acceptance is *by observation*: you run the artifact on a handful of inputs and
judge what you see. With a specification, acceptance is *by verification*: the
artifact belongs to the set of things a deterministic validator accepts. And the
validator has a property the generator does not: it is monotone. Strengthening
any check shrinks what gets accepted without touching the model. Quality
improvements compose through the deterministic boundary, not through
retraining. That is section 16 in one sentence, and it is why this guide says so
little about which model to use.

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

## 9. The principles underneath

Everything so far has been mechanisms: clarification markers, ratchets, gates,
three positions on a spectrum. Mechanisms date. The tooling that carries them
will have been replaced twice before this decade is out, and a guide that is only
an inventory of current practice ages into a museum piece.

So it is worth separating the mechanisms from whatever generates them. What
follows are seven principles that the rest of this guide is an instance of. None
of them mentions a tool, and none of them stops being true if the models get
twice as good. Keep these and lose every tool named here, and you can rebuild the
practice. Keep every tool and lose these, and you have the appearance of rigour
that the previous sections keep warning about.

### One: intent must be an artifact, not an event

A conversation is an event. It happens, it ends, and what it settled survives
only in whatever somebody happened to write down afterwards. An artifact
persists, has an address, can be cited in an argument, and can be contradicted by
a person who was not in the room.

*Generates:* the repository in section 13, the insistence that a chat log is not
a specification, and most of section 1.

*What it costs:* writing things down, and the discipline to do it at the moment
the decision is made rather than at the moment somebody asks.

### Two: a system that cannot record uncertainty will manufacture certainty

This is the generalisation of `[NEEDS CLARIFICATION]`, and it is not a fact about
models. Any process whose output format has no slot for "undecided" produces
documents with no undecided parts, because the format demands an answer and
somebody, or something, supplies one. Models make this fast and visible. They did
not invent it: a requirements document with no open questions section has never
in the history of the practice meant that there were none.

*Generates:* clarification markers, the blocking question in the Clarify phase,
the `pending` row in the coverage matrix.

*The test:* can your artifact say "I do not know", and does anything downstream
refuse to move while it does?

### Three: authority attaches to ratified decisions, not to formats

No document is normative because of where it lives or what it is called. It is
normative because somebody with the standing to decide has ratified it and the
ratification is recorded. This is why section 14 refuses to let a test win an
argument on the grounds of being executable, and why a wiki page can be
authoritative while a YAML file is gossip.

*Generates:* the ratification step, decision records, the conflict rules.

*Where teams get this wrong:* they install a format and believe the authority
arrived with it.

### Four: whoever does the work must not own the oracle

The single structural property that separates a ratchet from a ritual. If the
same actor can produce the implementation and adjust the thing that judges it,
the judgement carries no information, and it does not matter whether that actor
is a model or a person in a hurry on a Friday.

*Generates:* point three of the ratchet, the separation table in section 8, the
permission boundaries in section 16.

*Note the generality:* this is the oldest idea in the guide. Double-entry
bookkeeping, peer review and the separation of powers are the same principle, and
none of them was designed with software in mind.

### Five: closure is computed, not declared

"Done" is a claim. Closure is a verdict, derived from conditions a program can
evaluate. The distinction survives any amount of improvement in whoever is making
the claim, because the problem was never that the claimant is unreliable. It is
that a claim and a verdict are different kinds of thing.

*Generates:* the closure formula in section 15, the gate, confirm red.

*The corollary people skip:* if you cannot compute it, you have not defined done.
You have described a feeling about done.

### Six: use the minimum rigour that removes the ambiguity

Piskala's rule, promoted here to a principle because it is the one that stops the
other six metastasising. Rigour is a cost paid to remove a specific ambiguity.
Where there is no ambiguity there is nothing to buy, and the ceremony failure in
section 3 is what happens when a team forgets the "minimum" and keeps the
"rigour".

*Generates:* the spectrum in section 7, and permission to do almost none of this
on most changes.

*Its enemy:* it is the only principle here that cannot be enforced mechanically,
because a gate that checks whether you have too many gates is a joke with a
maintenance burden.

### Seven: the artifacts are the prompt

Whatever you write down is read by the thing that writes the code. Headings
decide what gets thought about, order decides what gets thought about first, and
prohibitions are the only part of the process that acts before the mistake
exists. Section 11 works this through; as a principle it means something
uncomfortable, which is that your templates are model behaviour and your process
documents are executable whether you intended them to be or not.

*Generates:* templates as constraints, the constitution, the whole of section 11.

*The trap:* a prompt is a request. Section 11 is also where that gets said.

### The principles are not all compatible

A list of principles that never conflict is a list nobody has used. Two tensions
are worth naming, because you meet both in the first month.

**One against six.** Every decision is worth an artifact, and most decisions are
not worth the artifact. No formula resolves this, only the test in section 3:
will somebody have to change this without having written it?

**Three against five.** Authority is human and closure is mechanical, so there is
always a band of things a person has ratified and no program can check. The
honest response is to make that band visible rather than pretend it is empty. A
requirement with no computable oracle is not a defective requirement, it is a
requirement whose verification is a person, and the row should say so instead of
sitting at `pending` forever looking like unfinished automation.

| Principle | Mechanism it generates | What you get without it |
|---|---|---|
| Intent is an artifact | The repository, the change record | Archaeology |
| Uncertainty is representable | Clarification markers, `pending` rows | Confident guesses, invisibly |
| Authority is ratified, not formatted | Ratification, the conflict rules | Whoever edited last wins |
| The worker does not own the oracle | The ratchet, permission boundaries | A green build that means nothing |
| Closure is computed | The closure formula, the gate | "Done" as a mood |
| Minimum rigour | The spectrum | Ceremony |
| The artifacts are the prompt | Templates, the constitution | Somebody else's opinions, enforced silently |

---

## 10. The adjacent layers

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

The fashionable objection runs the other way: if the whole codebase fits in the
window, why write a specification at all? Fontoura gives the short answer, and
it is the right one. Context length and context precision are different
problems. A million tokens of code tell the model what the system *is*. They say
nothing about what it should *become*: the intent, the constraints, what is
deliberately out of bounds. A bigger window makes the agent better informed
about the present and no wiser about the target, and gives it more surface from
which to copy the wrong precedent. Context makes the agent aware. The
specification makes it aligned.

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

A phase machine of the kind described in section 15 is a *clever* loop, and clever
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
more useful. The box in the third row, the harness, is the one this guide comes
back to: section 16 is about building it.

The reason this section comes before the tools is that it explains what to expect
of them. Most tooling in this space is strong at one or two layers and silent
about the rest, and no product covers the layer where authority lives, because
authority is not a feature.

---

## 11. The template is a prompt

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

Palacio gives the category a name, and the name helps defend it against anyone
who reads "documentation" and thinks of the Agile Manifesto. Until now a
project's documentation came in two kinds: informative, so that a person can
understand the system, or administrative, to satisfy a process. The
specification an agent consumes is a third thing, *operative documentation*. It
informs nobody about the software; it produces it. The manifesto's second value
was written against the first two kinds, and this one did not exist in 2001.

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

There is also a measured reason why a longer template does not buy more
compliance. The work on the *curse of instructions*, which Palacio's guide
picks up, measured what happens when verifiable instructions are stacked into
one prompt: the probability of satisfying all of them fits rather well to the
probability of satisfying one, raised to the number of instructions. Ten rules
at ninety percent reliability each and the set holds one time in three. The
consequence for templates is direct: decompose rather than accumulate, and put
first whatever must not fail. The consequence for section 16 is the same:
instruction collision is not only a problem of contradiction, it is a problem of
quantity.

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

The word is already used for two things, and it helps to know which one you
are hearing. In the Scrum Manager guide, the "project constitution" is the
context file of section 4: conventions, stack, structure, what Spec Kit would
call the project file. In Spec Kit it is numbered articles that every plan is
checked against. Alenezi gives the second sense its exact place: in his model a
specification has four components, and one of them is *constitutional
constraints*, non-negotiable rules of security, privacy and regulation that the
static analyser checks, not a person. That is the answer to the question the
previous revision left open, what separates a constitution from a style guide
nobody follows: something executes it. A constitution that only the model reads
is a style guide by another name. One that a validator checks is an article of
the gate. Marri reports a 73% reduction in security defects with that
arrangement; it is a single project, with the same developer under both
conditions, and section 19 says what weight to give it.

So: read the ones you adopt. The three gates in section 8 and
the articles above are not neutral scaffolding. They encode a specific view about
project structure, abstraction and testing, and the parts that are wrong for you
will otherwise be enforced silently for as long as nobody notices.

---

## 12. How legal requirements are served by this

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

## 13. One repository, four representations

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

Fontoura arrives at a similar partition from practice, and the convergence is
the useful part. Three layers, each with a different lifespan: an entry file of
under thirty lines that only routes, a directory of durable context that
changes when an architectural decision is made, and a folder per feature with
the change's documents and its state. Each layer fails without the other two.
And a precedence rule that section 14 adopts: durable context does not silently
override an approved specification; if they conflict, the agent stops and asks
which of the two artifacts to update.

The test of whether you have built this properly: **if you uninstall the note-taking
app, does everything still work?** The artifacts should be readable as plain
markdown, validatable by a script, versionable with Git and checkable in CI. If
they are not, you have built a personal wiki with extra steps.

---

## 14. When artifacts disagree

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

Fontoura states this as the survival rule of the method, and it deserves the
imperative: *never patch the code and leave the spec behind.* It is not only
that the specification ages. It is that when the module is regenerated, the
patch disappears and the bug comes back, because the constraint lived in your
head and not in the document. His example is the one that best shows what a
ratification is: a charge specification passed requirements review and reached
design without the uniqueness constraint on the idempotency key. The design was
coherent and it was wrong. A person reading the document caught it, not a
check, and that is why ratification in section 15 is a phase and not a
checkbox: it is a reading.

---

## 15. The loop

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

The "verified" row needs a format, or it becomes a claim under another name.
The one Fontoura uses fits in five lines and is the one to insist on: the claim
being checked, the command that ran, the exit code, a one-line summary, and the
verdict. Three rules keep it honest. Verification scope is proportional to the
claim: a narrow claim runs one test; "the feature is done" runs everything. If
there is no command, say so: "verified manually in the browser, no automated
test" is an honest report and "it works" is not. And no row closes on
yesterday's evidence: the code has changed since, which is what the formula
above means by "this exact commit".

---

## 16. Harness engineering

Section 10 gave the loop a single row in a table and said its state lives "in the
harness". This section is about that box, because it is where most of the
distance between a demonstration and a system actually sits.

A caveat on the name first, in the spirit of section 10. "Harness" is settled
usage: it is what the agent tooling community calls the program around the model,
and nobody argues about it. "Harness engineering" as a named discipline is not
settled, and presenting it as one would overclaim in exactly the way that section
warns against. Read it as a scope of work rather than as a field.

> **The harness is everything that decides what the model sees, what it can do,
> and what happens to what it produces.**

The claim that earns it a section: **the model is the least controllable
component in the system, and it is the one everybody tries to control first.**
Prompt tweaks and model upgrades are the two levers that come to hand, and they
have the worst ratio of effort to variance removed. Everything else is ordinary
software, which means it can be specified, tested, versioned and reasoned about,
and almost nobody does any of that to it.

### What a harness contains

| Component | Decides | What its absence looks like |
|---|---|---|
| Context assembly | What the model sees this turn | Rules obeyed on Tuesday and forgotten on Wednesday |
| Tool surface | What actions exist at all | Inventive solutions to problems you did not know were reachable |
| Permissions | Where writes may land | A test suite that agrees with the implementation |
| Control loop | Continue, retry, stop, escalate | Runs that end when the money does |
| Oracles | Who says it worked | "Done" |
| State | What survives a crash | Work that cannot be resumed, only restarted |
| Budget | What it costs before a person looks | The invoice as the first signal |
| Record | What happened, reconstructible later | An outcome nobody can explain |

Two things about that table. Only one row is about the model. And every row is
ordinary engineering that nevertheless goes unreviewed in most teams, because a
harness arrives as glue, and glue is not perceived as a component. A harness is a
program. It has a specification or it has undocumented behaviour, and section 1
already described what happens after that.

### Designing one from scratch

The instinct is to start with the loop, because the loop is the interesting part.
It is the wrong end. A loop is defined by its exit condition and its exit
condition is an oracle, so a harness designed loop-first arrives at a loop that
runs until the model says it is done.

Build in this order.

**1. Name the unit of work.** A unit is what one iteration is expected to close.
Get it wrong and everything above it misbehaves in ways that look like model
problems: a unit too large never closes and sits at `pending` forever, a unit too
small spends its whole budget re-establishing context. This is Ralph's variable
from section 10, and it goes first because every later decision depends on it.

**2. Write the oracle for one unit.** Before any orchestration exists, answer
this: what program, run by somebody who does not trust me, decides whether this
unit is finished? If there is no answer, stop. You do not have a harness problem,
you have a specification problem, and building the harness first produces an
efficient machine for arriving nowhere in particular.

**3. Put the state on disk.** Whatever the next iteration needs to know must be
readable from the filesystem rather than held in an orchestrator's memory. This
is the Ralph argument from section 10 and it is a durability requirement, not a
preference: a harness whose state lives in a process loses a day of work to a
dropped connection.

**4. Define the tool surface, and keep it small.** Every tool is a decision the
model now gets to make. Tools are not free capability, they are branching factor.

**5. Set permissions before the first run, not after the first incident.** Which
paths are writable in which phase. The one people forget is not production, which
everybody remembers, it is the oracle, which stays writable until somebody has
watched a suite go green for the wrong reason.

**6. Now write the loop.** Entry condition, exit condition, retry policy,
escalation exit. It should be dull. If your loop is interesting, some of that
cleverness is state that belongs on disk.

**7. Add budgets, then the record.** A turn limit and a token budget per unit,
and an append-only log of what ran, on which inputs, with which verdict. The
record is what makes an incident answerable six weeks later, which is the thing
section 1 says you lose first.

The honest note to end on: a minimum viable harness is a shell script, a
directory of files and a test command. Most teams reaching for an orchestration
framework have not yet written down their oracle, and a framework does not supply
one. It supplies retries, which is how a missing oracle becomes an expensive
missing oracle.

### Reducing errors without changing the model

Same weights, fewer defects. This is the part of the work with the best return
and the least literature. The levers are roughly in order of what they buy for
what they cost.

**Make the bad output unsayable.** Constrained or schema-guided decoding, from
section 10. Moving a constraint from *rejected* to *cannot be emitted* deletes a
class of retry rather than handling it. Anywhere the model must choose from a
known set this applies, and the known sets are more common than they look:
statuses, identifiers, file paths, phase names.

**Shrink the decision surface.** Fewer tools, each narrower. One tool that does
the right thing beats one tool with a flag selecting between the right thing and
a footgun. The same goes for any configuration the model can see: every option is
an opportunity to pick the other one.

**Make failures instructive.** The cheapest large win available to most teams and
the most consistently skipped. When a check fails, what the model reads next is
your error message, and that message is a prompt whether or not anybody wrote it
as one. An exit status of 1 produces guessing. *"FR-002 violated: balance 60000
exceeds MAX_BALANCE 50000, see specs/FR-002.md"* produces a fix, because it names
the rule, the observation and where to look. Error text is the highest-traffic
prompt in the system and usually the only one nobody has edited.

**Put the invariant first and the variable last.** Ordering for the provider's
prefix cache, from section 10, and for salience at the same time. It saves money,
and it makes the stable rules the thing the model has seen most.

**Separate the sessions that are meant to disagree.** A review performed in the
session that wrote the code inherits the reasoning that produced the bug.
Different session, and where it matters different permissions: principle four,
implemented with process boundaries.

**Make retries earn their place.** The rule from section 10, restated as a
harness setting: a retry is granted only when the input contains something new.
Same failure signature and no new hypothesis means escalate, not repeat. Without
this rule, a loop with a budget is a slower way to spend it.

**Checkpoint at unit boundaries.** A failure should cost one unit of work rather
than a session. State on disk again, seen from the cost side.

**Take determinism wherever it is available.** Not from the model, from
everything around it: pinned dependencies, fixed clocks, seeded generators,
recorded fixtures. The aim is not reproducible generation, it is attributable
failure. If a harness is non-deterministic in six places, no failure can be
localised to the one place that is non-deterministic on purpose.

Now the counterweight, because this reads too easily as a promise that
scaffolding substitutes for capability. It does not. The test for whether you
have hit the ceiling is: **would a competent person, given this context and these
tools, succeed?** If yes and the agent fails, it is a harness problem and the
levers above apply. If no, you have a decomposition problem dressed as a harness
problem, and more scaffolding buys more expensive failure.

There is also a way for a harness to make things actively worse, and it has a
recognisable shape: **instruction collision.** A project file says one thing, a
skill says a second, an injected template says a third, and none of the three
authors knows the other two exist. The symptom is behaviour that varies between
sessions for no visible reason, and the reflex, adding a fourth instruction
telling the model how to prioritise the first three, is Böckeler's
*Verschlimmbesserung* arriving on schedule. The fix is dull: one authority per
question, and a periodic read of everything the model is actually sent, which is
a thing remarkably few teams have ever looked at in full.

### Validating an agent's work automatically

"Automatically" carries a lot of weight in that question, so split it. Automatic
checking of *compliance with something already agreed* is largely a solved
engineering problem, and the rest of this section is about doing it well.
Automatic checking of *whether the agreed thing was right* is not solved, is not
close, and any tool claiming otherwise has moved the judgement somewhere you
cannot see it.

An oracle is whatever produces the verdict. They differ in what they can catch.

| Oracle | The verdict it gives | Its blind spot |
|---|---|---|
| Schema or contract | The shape is legal | Says nothing about meaning |
| Ratified example | This named case matches an agreed answer | Only the cases somebody wrote |
| Property | A rule held across generated inputs | Easy to state vacuously, hard to state well |
| Metamorphic | Two related runs relate as they should | Needs a relation you can name |
| Differential | The new thing agrees with a reference | Inherits the reference's bugs |
| Replay | The same inputs produced the same outputs | Consistency is not correctness |
| Types and static analysis | A class of defect is absent | Absence of a class, not presence of intent |
| A model as judge | A fast, cheap opinion | Not executable in section 8's sense |

That last row is the tempting one and the most often misused. A model reviewing a
diff is genuinely useful: good triage, catches things people skim past, costs
almost nothing. It is not a gate. It is not reproducible, it can be talked out of
its position by the thing it is reviewing, and a check that returns a different
verdict on Tuesday is a notification with extra steps. Use it to decide what a
person looks at. Do not use it to decide what merges.

There is a stronger version of principle four that the table does not capture,
and it is worth knowing even though almost nobody can afford it. Ryan describes
StrongDM's arrangement, which has been producing software since 2024 with three
engineers and nobody writing or reviewing code: the evaluation scenarios live
*outside* the repository and the agent never sees them. It is not that it
cannot edit the oracle; it does not know what the oracle contains, like a
validation set a model has not seen during training. An agent that can read the
tests can, under optimisation pressure and without any ill intent, write code
that passes them without doing what they were meant to check. With a hidden
oracle that route does not exist. The second component is what makes the first
possible: behavioural replicas of every external service, so the agent develops
against simulated environments and touches no real data. For most teams that is
a direction, not a recipe. The minimum recipe remains the previous rule: the
oracle is not writable while implementation is under way.

Three rules make the rest work.

**An oracle the agent can edit is not an oracle.** Principle four, expressed in
file permissions. During implementation the expectations are not writable. A
change touching an implementation and its expectations in one commit is a review
trigger by construction rather than by somebody's vigilance. Everything else in
this section depends on this rule, and it is the one relaxed first, because
relaxing it makes a red build go away.

**Confirm red is how you test the oracle.** The discipline in section 15 usually
gets read as a test-first rule. In harness terms it is more precise than that: it
is the only cheap check that the oracle observes what it claims to observe. An
expectation that passes before the implementation exists is not evidence, and the
three explanations for it, that the behaviour already existed, that the test does
not observe what it says, or that the specification describes the system wrongly,
are all things worth learning before writing the code rather than after shipping
it.

**Assume the suite is decorative until something proves otherwise.** "Are these
tests worth anything" has a mechanical answer: change a constant in the
implementation and see whether anything goes red. Mutation testing automates
exactly that, and it is the closest thing available to an oracle for your
oracles. Expensive across a whole codebase, cheap across the twenty files
implementing your ratified rules, which is the only place the answer matters.

And the boundary, stated plainly, because a section on automatic validation that
omits it is selling something. No oracle tells you whether the specification was
right. None tells you whether an abstraction is the right size, which is why
section 8's shape gates are questions put to a person rather than assertions run
by a program. None tells you whether a legal requirement was read correctly. The
harness's job with all three is not to decide them. It is to route them to
whoever decides, while it is still cheap, and to refuse to close while they are
open.

### Building agentic flows

The first question is the one people skip, because both answers get called the
same thing in marketing material.

> **Enumerate the decision points. If you can enumerate them, write a workflow.
> If you cannot, you need an agent, and then you need to bound it.**

A workflow's control flow is written by you and is inspectable before it runs. An
agent's is decided at runtime, which buys adaptability and costs you the ability
to know in advance what will happen. Most production systems described as agentic
are workflows with one or two genuinely agentic steps inside them, and that is
usually the right shape rather than an admission of timidity.

Whichever you have, five rules keep it from decaying.

**Phases are states, with entry and exit conditions.** Not stages on a diagram. A
phase you can enter without meeting a condition is a label, and unless the exit
condition is an oracle the phase does not end, it gets abandoned.

**Handoffs carry artifacts, not conversation.** The next phase reads files. If it
needs the previous phase's reasoning then that reasoning is an artifact now, and
principle one applies. Passing a transcript forward feels like continuity and is
how a flow acquires a dependency on a context window nobody controls.

**Roles have different write permissions.** The proposer writes specifications,
the implementer writes source, neither writes evidence. Justified twice over, as
section 10 points out: context hygiene wants it and separation of duties requires
it.

**Human checkpoints are states, not interruptions.** Ratification is a phase in
the table in section 15 for exactly this reason. A checkpoint modelled as an
interruption gets optimised away as friction, because friction is what it looks
like on a dashboard. A checkpoint modelled as a state has an entry condition, a
queue and a latency, all of which can be measured and argued about. Palacio
gives the practical reason, which is approval fatigue: an agent that asks
permission for every change produces dozens of interruptions per session, and
people respond by approving without reading. Concentrating review at the gates
between phases, where the information is worth most and correction costs
least, is what lets the implementation phase run with little intervention.

**Every loop needs a named exit that is not success.** Escalate, and say to whom,
with what. A flow without one finds its own exits, and the ones it finds are
exhausting the budget, exhausting the context, and declaring success. The third
is the expensive one. Alenezi states it as a property of the loop and the
statement is the right one: exhausting the budget escalates to a person rather
than silently lowering the bar.

Put together, that is what the phase table in section 15 is: a state machine
whose state lives in files, whose transitions are guarded by oracles, and whose
write permissions differ per phase. Written out as a harness specification, it
looks like this.

| Phase | Writable by the agent | Transition requires |
|---|---|---|
| Propose | Proposal drafts | Schema valid, cited IDs resolve |
| Clarify | The question list | No blocking question unanswered |
| Ratify | Nothing | A recorded human approval |
| Evidence | Expectation drafts | Human approval of the expected result |
| Confirm red | Nothing | The new evidence fails |
| Implement | Source paths only | Build passes |
| Verify | Source paths only | Every required row verified, CI green |
| Integrate | Nothing | The closure formula evaluates true |

The middle column carries the argument. Two phases where the agent writes nothing
at all are what stop the loop being a closed circuit, and they are the first two
to get quietly widened when a team is behind schedule.

Palacio expresses the same table from the agent's side, with three levels any
project file can adopt as they stand: *always*, what gets done without asking,
such as running the tests before a commit; *ask first*, what may be right but
has impact, such as touching the schema, adding a dependency or changing the
public API; and *never*, the red lines, such as committing secrets, deleting a
failing test or stepping outside the task's scope. The useful part is not the
examples, it is that the scheme separates autonomy from permission: the
*always* level exists so the agent does not interrupt for every micro-decision,
and the *never* level removes whole categories of error rather than detecting
them. And it is a frame that moves: something goes from *ask first* to *always*
once the team has watched the agent decide well in that area. The permissions
in the table above are the same thing with one difference: the project file
asks for it and the harness enforces it.

### What each gives the other

This is not a relationship between a methodology and its tooling, and it reads
better in both directions.

**Specification work gives the harness what it cannot compute for itself:** an
exit condition that means something, which is ratified obligations rather than
the model's own sense of completion; a state model that is already designed,
since the coverage matrix is the loop's state; a reason for the permission
boundaries that is not paranoia; and a defined escalation trigger in the
clarification marker.

**The harness gives specification work the only thing that makes it real:** a
gate needs something that actually runs, actually blocks, and cannot be bypassed,
and all three are harness properties. Section 8 defines what a gate is. The
harness is where "mandatory" stops being an adjective.

And Alenezi's argument for putting human judgement upstream rather than
downstream is the most forceful I know, because it appeals to arithmetic rather
than to virtue. A person reviewing generated code at the speed it is generated
is the bottleneck and the weakest link at once, and the second half is
measured: people reviewing with an assistant beside them write less secure code
and are more convinced of the opposite. The scarce resource goes where it has
the most leverage, authoring the contract and handling escalations. The volume
of checking is done by the validator.

Which is the sentence to take away from this section:

> **A specification without a harness is a wish. A harness without a
> specification is an efficient way to converge on nobody's intent.**

---

## 17. Where the specification comes from

The loop in section 15 begins at capture, with "the literal request".
Everything after that takes it for granted that somebody wrote the sentence.
Seyff and Glinz, in a 2026 position paper, point at what that assumption hides:
the practice "is largely silent on where those specifications come from". The
tooling assumes a developer writes them, alone with an assistant. The SpecMine
census confirms the shape: the specification is written by a developer or, "more
often", drafted by an AI tool and then touched up by the developer.

Read that slowly, because it is the weakest part of the whole arrangement. The
most important artifact in the process is drafted by the person with the least
access to what the business wants, with the help of a model that has
inclinations of its own. The earlier sections govern what happens to a
specification once it exists. This one is about the two failures that happen
before.

### Disambiguating too early

Seyff and Glinz put it in a sentence worth keeping: *premature disambiguation
can be a defect rather than a virtue.* If the model resolves every
underspecified element by guessing, it locks in interpretations that the
stakeholders never had the chance to validate. Their rule for assistance in the
early phase is that it should flag underspecification rather than resolve it
silently: "this element appears in three places with different relations; is
that intentional?".

It is principle two seen from the other side. It is not enough that the
artifact can say "I do not know"; the step that drafts it has to be allowed to
leave things open, and a template that demands a value in every field takes
that permission away. It connects to the cost section 3 called premature
commitment, and to Hill's distinction that section 19 picks up: a specification
written before anything has been validated is a guess with structure. For what
you already understand, the order "specification first, then code" is right.
For what you do not yet understand, the honest specification is written after
the prototype and before the second version.

### The drift towards the average system

The second failure is subtler and has no name in the specification literature,
though it has one in modelling. Language models carry strong priors towards the
standard notations, UML, BPMN, entity-relationship diagrams, and more generally
towards the most frequent shape of a problem. Seyff and Glinz call it
homogenisation: without countermeasures, model-assisted projects drift towards
the same handful of patterns. Translated to specifications, a draft written by a
model drifts towards the average system, which is not yours. Their
countermeasures are concrete: restrict retrieval to the session's context,
penalise imported vocabulary, and an explicit "stay inside our language" mode.

This guide's version is a reading test. The vocabulary of the specification has
to be the business's. A draft that arrives with words nobody in the room uses is
a draft that has imported another system, and the six questions in section 5
get answered on their own, with somebody else's answers, without anyone
noticing.

### Three design rules that were already here under other names

The authors propose principles for AI assistance in that phase, and three of
them are things this guide holds from another angle, which suggests they are
properties of the problem rather than of the tool.

*Propose, never impose.* Every assignment, every structural change, is a
suggestion the person accepts, modifies or rejects. It is "the agent proposes, a
person ratifies" applied before a requirement exists.

*Visible and reversible inferences.* Every inference the model makes is a
first-class event in the model's history, and it can be undone. It is principle
one applied to the drafter's decisions, not only to the business's.

*Traceability of every inference to its origin.* Every proposed type, every
inferred rule, has to point at the element it came from, and in practice that is
enforced by requiring every proposal to cite at least one source element by
identifier. This is the one the guide did not have as a check and should. In
the repository of section 13, every requirement derives from an intent. A
requirement whose `derives_from` is empty is a requirement the drafter invented,
and a validator can refuse to ratify while one exists. It is a cheap check for
the one class of invention section 5 cannot see: the kind that arrives already
dressed as a rule.

### The interview

There is a more mundane technique that most teams can apply tomorrow, and
Fontoura takes it from Anthropic's documentation: before writing anything, ask
the model to interview you. Not the obvious questions; the hard parts you have
not considered, edge cases, trade-offs, and only then write the specification.
Then implement in a clean session, so the implementation follows the document
and not the conversation that produced it.

It is the clarify phase of section 15 run before the proposal rather than after,
and it works for the same reason the marker does: it turns into questions what
would otherwise be assumptions. With a limit that section 1 already noted: an
interview produces answers at the speed a person can give them, in the heat of
the moment. The marker preserves the option of not answering yet. A good
interview ends with some questions unanswered, written down, and the state token
unchanged.

---

## 18. When the spec has more than one reader

Everything so far holds for one person and one agent. In a team the
specification keeps that job and picks up two more, and missing that is how you
end up with a folder of specifications nobody reads and a ritual nobody believes
in.

| The specification sits between | What it carries |
|---|---|
| A person and the agent | The only memory the agent has, and what bounds its drift |
| One person and another | What a colleague reads instead of reading your mind |
| One team and another | The contract at the boundary where two teams integrate |

The trap is treating a team specification as a solo specification with more
authors. You keep writing private notes, give them a shared folder and call it
a practice. The notes still assume everything in your head. A colleague opens
the file, hits the first implicit rule and guesses, which is exactly the
problem specifications exist to kill. The test in section 3 applies as it is:
your colleague and the agent have the same handicap, neither was in your head.

### The argument moves to the cheapest layer

The rule that turns a folder into a team practice is the one least often
written down, and Fontoura writes it down: **the specification enters review
before the code exists.** The requirements arrive as a pull request, somebody
reads them, and only when they approve does the state change and design begin.
The same for the design. The same for the tasks.

A code review after implementation catches typos in a decision that was already
wrong. A specification review catches the wrong decision before a line encodes
it. The most expensive review a team does is the one afterwards, when the
disagreement is about a finished thing.

| Where the disagreement shows up | What it costs to resolve |
|---|---|
| In the requirements pull request | A comment thread, before any code exists |
| In code review | Rewriting a feature that already works |
| At integration, between teams | Two implementations that do not fit |
| In production | An incident, and then all of the above |

The value of the specification in a team is not documentation. It is moving the
argument to the layer where having it costs least. A team with specifications
does not disagree less. It disagrees earlier.

### Reviewing a document is not reviewing code

Palacio makes an observation that looks minor and is not: the gates before
implementation review text, not code, and that changes who can take part and
what is being asked. More people can read a specification than a diff: whoever
knows the business can say whether the requirements are the right ones without
being able to program. And the two questions that compete in a code review, "is
this what we want?" and "is it well built?", come apart: the gates before answer
the first, the verification after answers the second. Two focused reviews tire
people less than one that tries to do both.

On who approves, Palacio's answer is the right one: it depends on the team, and
what matters is not the role but that approval is a deliberate, explicit act.
Somebody reads the artifact, evaluates it against known criteria and decides
whether it is enough to move on. Whoever knows the domain approves the
requirements. Whoever knows the code approves the decomposition into tasks,
which is the most technical gate and the one where developers are worth having.
And somebody watches the gates themselves, so they are neither skipped under
schedule pressure nor turned into a bottleneck because the approver is away.

### The canon lives in the tool

Solo, your conventions live in you. In a team, if they live only in heads, each
developer drifts in their own direction and you end up with five dialects of
specification that read nothing alike. The fix is principle seven in its
organisational form: the canon goes where the tool reads it. The durable
context of section 13 with the whole team as author and reader, the templates
and skills that carry the format and the bar to everyone's machine, and the
conventions written down: when a change needs a specification, what the format
is, who approves each gate.

This changes onboarding too. A new person reads the specifications and the
durable context, not a wiki page and a colleague to ask. A convention that lives
in the most senior person's memory scales to exactly the number of people that
person can correct in person. One encoded in a file scales to everyone who runs
the agent, including the agent.

### The gate has to be physical

Solo, you read the state token yourself. In a team, a gate that lives only in a
file nobody opens is a gate that gets skipped, because most people cannot see
it. Fontoura puts it on a board: one column per phase, one card per change, and
the card moves when the gate is approved. Approving *is* the move. With one rule
that stops the board becoming a second source of truth: Git holds the artifact
and the board reflects the state; the card points at the specification, it does
not copy it.

And the gate gets muscle from what section 8 calls mandatory policy, now applied
to people: branch protection refuses to merge without a review. The gate has to
be physical, not a norm people remember on their good days.

### The bottleneck moves

The reason all of this pays for itself in a team has nothing to do with typing
speed. Solo, your bottleneck was your own loop. In a team, generation gets cheap
fast, because everyone has an agent, and the team can produce several times more
code than before. What ships does not grow at the same rate, because the wall
has moved: it is now in review, in deployment and in the coordination between
people and teams. Fontoura puts it in a sentence that deserves the emphasis:
**generation is cheap; integration is the job.**

The one enterprise case Alenezi cites points the same way from the other side,
with the caveat that it is a single case: one engineer with four specialised
agents delivered an initiative sized for a four-person team, and the most
consistent gain came not from generating faster but from collapsing the outer
loop of coordination between disciplines, because a shared specification was
the one referent everybody looked at. A board with a work-in-progress limit on
the review column makes that wall visible: the cards pile up there, and no
faster agent clears them.

### How it fails in a team

Palacio catalogues the ways this goes wrong while appearing to go well, and
three are worth watching from the first month.

**Specification theatre.** Specifications get written and gates get run, but
the review is superficial and the signature is a formality. The cause is
usually one of two: schedule pressure, or specifications so generic that
reviewing them adds nothing. The answer is not more discipline; it is either
better specifications or less process on the changes that do not need it.

**Zombie documentation.** The project accumulates specifications nobody
consults, nobody updates and nobody deletes. It is the anchored mode adopted
without a maintenance process: rigour in the first cycle, abandonment in the
next. Deciding consciously which specifications are kept and which are thrown
away after implementation is part of the work, and a specification that is kept
has an owner.

**The specification as a control tool.** Every decision has to pass a gate and
the builders' autonomy disappears. It confuses the structure of the process
with control of the team. The *always* level in section 16 exists precisely so
that routine decisions need no approval; if the team feels the gates limit it
rather than support it, the calibration is wrong.

---

## 19. What the evidence says

The previous revision of this guide ended with a warning: none of this is
demonstrated. Since then somebody has measured it, and the result is not
flattering. This section exists because a guide that argues for a practice owes
its readers the best argument against it, and there is now one with data.

### The study

Hill, in a working paper from April 2026, analyses 100,247 merged pull requests
across 119 open-source repositories. He derives five hypotheses from the
vendors' literal claims, mostly Spec Kit's and Kiro's: that specifications
reduce defects, that they reduce rework, that better specifications produce
fewer defects and less rework, and that they constrain the scope of AI-generated
code. He traces defects back to the commit that introduced them and compares
each author with themselves, their changes with a specification against their
changes without one, which is the most conservative design available for
observational data.

None of the five holds. Within author, changes with a specification carry more
defects (1.4 points more, at the edge of significance) and more rework (5
points more, with p below 0.001). Specification quality, scored on seven
dimensions copied from the tools' own templates, has an effect on rework of
exactly zero. And the scope-constraining effect on AI-tagged changes does not
appear. Four robustness checks, with other outcome measures, with the classic
defect-prediction features, dimension by dimension and at repository level, say
the same. Adding "has a specification" to a defect-prediction model improves
its fit by 0.000014.

The author's reading is the one from medicine: confounding by indication. The
hardest, largest, riskiest tasks are the ones that get a specification, and they
are also the ones that produce the most defects, so the specification marks
difficulty rather than reducing it.

### What it does say, and what it does not

The limits are listed by the study itself, and they are the ones an honest
reader would note. It is all open source, in a convenience sample. The measure
of "has a specification" is deliberately loose: a linked issue counts. Quality
was scored by a language model. And most of the data predates agentic
workflows: only 2,650 pull requests carry an AI tag, and among those the
specification shows no effect in either direction; the subset closest to the
workflow the tools sell, high-quality specifications on AI-assisted changes,
gives 4.8 points fewer defects over 42 authors, which the author calls
suggestive and not robust. So the best available evidence says the advertised
benefit is not visible, it does not say the practice is useless, and it does
not yet observe the workflow it is most aimed at.

What the study does to the marketing claims is final, and what it does to this
guide is different, and the two should be kept apart. The argument of section 1
was never "fewer bugs". It was that somebody can answer, six weeks later, why
the system does what it does and who agreed to it. Hill reaches the same place
from the data: specifications "create value after code ships, not during
generation", as an audit trail and as documentation that outlives whoever wrote
it. And he adds the sentence that sums up better than anything in this guide why
generation does not solve the problem: *the specification tells the AI what to
build; it does not tell the AI what it forgot to specify.* The hard part is not
solved, it is relocated.

That this guide survives the study because it never promised what the study
refutes is a defence, and also a weaker claim, and it should be stated as one:
what is defended here is who answers for what and what can be reconstructed,
not a defect rate.

### The 50% chain

One detail of the study this guide has to record, because it is its own warning
about inherited citations coming true. Piskala claims that "controlled studies"
show "error reductions of up to 50%". Hill followed the citation: it leads to a
Red Hat developer blog post and an InfoQ article, and neither contains a study,
an experiment or a number. It is practitioner opinion that acquired the look of
evidence by being repeated. The sources section of this guide already warned
that Piskala is a well-organised argument and not evidence; it is now also
known that the one figure it gives is nobody's.

### The numbers on the other side

The favourable numbers exist and deserve the same lens. Alenezi's reference
model carries in its abstract a 73% reduction in security defects under
constitutional constraints and a 50% reduction in time to market. In the body
of the paper the author himself classifies both as "unreplicated case
evidence" on which "the argument does not rest its weight": one banking
project with the same developer under both conditions, and one engineer with
four agents at a Brazilian bank. Read the abstract and then that paragraph, and
measure the distance. What the paper does have, and it is more useful than the
figures, is an honest counterexample: a preregistered experiment by Borg and
colleagues found no maintainability disadvantage in code developed with
assistants where conventional review discipline was in place. Alenezi's reading
is that the moderating variable is governance, not AI, and he marks it himself
as a hypothesis consistent with the data rather than a finding.

Fontoura contributes a practitioner case worth more for how he bounds it than
for its figures: thirteen applications, three APIs, around 138,000 lines and
1,650 tests, in seventy days, solo, over 28 specifications. The limits are his
own: it does not generalise, because the method externalises expertise and does
not manufacture it; speed was measured and quality was not audited; a deadline
was doing real work; and it is one data point with no control. His conclusion
is the right one: the method worked at that scale, once, for that operator.

### The critics of the trade

Two practitioner critiques circulate widely enough to cite. Scott Logic put
Spec Kit through its paces and found it roughly ten times slower than iterative
development, producing thousands of lines of markdown that still yielded buggy
code; they called it "reinvented waterfall". Zaninotto, from Marmelab's
production experience, writes that the practice shines when starting from
scratch and that, as the application grows, the specifications "miss the point
more often and slow development". Both are critiques of a tool's shape, one
workflow for every size, which sections 3 and 11 already make, and Palacio's
answer is proportionality: a one-line fix does not go through four phases. But
they should not be dismissed that fast. What both describe, the relation between
document volume and real change, is what Hill measures as rework, and it comes
out in the same direction.

### What is known about the problem, not the remedy

There is a second body of data the sources cite often and which needs placing,
because it is not about specifications but about AI assistance in general.
METR, in 2025, measured sixteen experienced developers on their own
repositories: with AI tools they took 19% longer and believed they had been 24%
faster. The 2025 DORA report, as Fontoura relays it, found 98% more pull
requests and 243% more incidents per pull request in teams using AI. Pearce and
colleagues found vulnerabilities in around 40% of code generated in
security-sensitive settings. This guide cites those three through other sources
and says so in the sources section. They establish the problem solidly: the
speed is real, the perception of speed is unreliable, and the failure rate rises
faster than the throughput. They do not establish that specification is the
remedy. That is what Hill went looking for and did not find.

### What is known about the practice itself

SpecMine, Carnegie Mellon's census from July 2026, is the first portrait of the
practice at scale, and it says three things a reader should hold in mind when
reading any claim about it. The practice is a year old: 99.7% of the 470,795
specifications were created in 2025 or later. Most of it is scaffolding: of
73,030 repositories, 923 have a hundred stars or more, and the census flags tiny
files, unfilled markers and placeholder text as signs of templates nobody
completed. And how a specification becomes code remains, in the authors' words,
an open question: 81.2% of pull requests that touch a specification also touch
code, but that is a heuristic, not an observation of the relation. The study to
wait for is the one that crosses that census with outcomes: how many markers
get resolved, how many specifications are abandoned halfway, and whether either
predicts anything.

### What to measure in your own team

Since no study yet observes your workflow, the measurement that matters is
yours. Palacio proposes a reasonable set, and this guide adopts it with one
change of emphasis. Flow: the ratio of specification time to implementation
time, the first-pass approval rate at each gate, and the deviation rate, how
often the agent stepped outside the specification's parameters and somebody had
to intervene. Outcome: first-pass quality, rework time and review time, which
with a clear contract should fall because review is against the specification
rather than against the reviewer's taste. And what not to measure: lines
generated and number of specifications; more specifications is not better.

The change of emphasis is this. The three outcome measures are exactly the ones
Hill found pointing the wrong way in his sample. If they point the same way in
yours, section 3 already said what follows: the structure has not earned its
place, and no loyalty is owed to a practice that worsens the figures it promised
to improve. What this guide asks you to measure in addition, and no study yet
does, is what it defends: how long it takes somebody to answer, about a change
from three months ago, what was decided, who approved it and what evidence
holds it up. If that number does not fall either, there is no excuse.

### The honest summary

The benefits being sold are not the benefits that have been shown. Fewer
defects and less rework have been looked for at scale and have not appeared.
Memory, attributable decisions and evidence that falls out of the process have
not been measured, and they are this guide's argument. And no study yet observes
the workflow in which the specification is an agent's primary input, which is
where the tools aim and where this guide lives. This section will age before
any other, and it is the one to reread at every revision.

---

## 20. What to take away

If you remember seven things.

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

6. **The harness is where "mandatory" becomes true.** Most of the distance
   between a demonstration and a system is in the program around the model, and
   almost none of that program is reviewed by anybody.

7. **The benefits being sold are not the ones that have been shown.** Fewer
   defects and less rework have been looked for across a hundred thousand pull
   requests and have not appeared. Memory, attributable decisions and evidence
   that falls out of the process have not been measured, and they are this
   guide's argument.

And one thing to be suspicious of, including in this guide: structure is cheap
to add and its benefits are mostly costs avoided, which are invisible unless you
measure them. If a team adds traceability and its defect rate and cycle time
both get worse, the traceability has not earned its place. Section 19 says what
has been measured already and with what result. What remains to be measured is
yours.

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
  inherited citations happening in front of us. And its one figure, "controlled
  studies" with error reductions "of up to 50%", leads to two blog posts with
  no study behind them, as Hill documents.
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
- Brenn Hill, *Does Spec-Driven Development Reduce Defects? An Empirical Test of
  Industry Claims Across 119 Open-Source Repositories*, working paper, SSRN,
  April 2026. Read in full. The only measurement at scale that exists, and the
  source of most of section 19. Its limits are listed by the author and this
  guide repeats them: open source, a convenience sample, a loose measure of
  "has a specification", quality scored by a model, and data that mostly
  predates agentic workflows. The data and the code are published, which is
  more than any other source on this list can say.
- Mamdouh Alenezi, *Specification-Driven Development as the Foundation of
  AI-Native Enterprise Software Engineering*, arXiv 2607.16680, July 2026. Read
  in full. A formal reference model, the specification as a tuple of functional
  obligations, quality thresholds, constitutional constraints and architectural
  structure, with a stochastic generator inside a deterministic validator. The
  source of "acceptance by observation versus acceptance by verification", of
  the validator's monotonicity, and of the argument about where to put human
  judgement. No data of its own; its corpus of 44 sources is verified one by
  one, and its section 6.4 weighs the evidence with an honesty the paper's
  abstract does not reflect.
- Shyam Agarwal, Anmol Singhal, Travis Breaux and Bogdan Vasilescu, *SpecMine: A
  Large-Scale Corpus of Spec-Driven Development Artifacts*, arXiv 2608.25202,
  Carnegie Mellon, September 2026. Read in full. A dataset, not a result: the
  census of the practice on GitHub, with counts of clarification markers and
  unfilled placeholders per document. The source of section 19's figures on the
  age and composition of the practice.
- Norbert Seyff and Martin Glinz, *From Sketches to Specs: AI-Assisted
  Lightweight Metamodeling for Spec-Driven Development*, position paper, MoDRE
  2026. Read in full. The source of section 17: the observation that the
  practice is silent about where specifications come from, premature
  disambiguation as a defect, homogenisation towards standard notations, and
  the design principles for assistance. No empirical evaluation, and they say
  so.
- Kevin Ryan, *Spec Driven Development: AI Native Software Engineering*, first
  edition, 2026, early beta. Only the first chapter exists and it is the one
  that was read. The source of Shapiro's five levels, of the StrongDM case with
  its external scenarios and service replicas, and of the reading that the
  bottleneck has moved. The METR and DORA figures this guide cites come through
  him and Fontoura, not from the originals.
- Juan Palacio, *SDD, Spec Driven Development: cuando el código es la
  consecuencia*, Scrum Manager teaching guide, version 1.0, April 2026. Read in
  full, in Spanish. Written with a model's assistance and says so. The source of
  "operative documentation", of the curse of instructions, of the three levels
  of boundaries, of approval fatigue, of the metrics table and of the
  anti-patterns in section 18. Also the source that reads the waterfall
  objection best. It uses "project constitution" for the context file, not in
  Spec Kit's sense, and section 11 points that out.
- Felipe Fontoura, *Spec-Driven Development: The Definitive Guide to Building
  Software with AI Agents*, 2026. Read in full. The source of the one-line state
  file and of "file existence does not imply approval", of the three context
  layers, of "confirm before building", of the verification report format, of
  the chapter on teams and of the thirteen-applications case, whose limits he
  writes himself. A practitioner's book with a kit to sell, and still the most
  careful of the practitioner sources in separating what it demonstrated from
  what it believes.
- François Zaninotto (Marmelab), *Spec-Driven Development: The Waterfall Strikes
  Back*, November 2025, and Scott Logic, *Putting Spec Kit Through Its Paces*,
  November 2025. Cited through Hill and Palacio, not read in the original. They
  are the two practitioner critiques section 19 records.

Three chapters are lighter on sources than the rest and it would be dishonest
not to say which. Section 9 distils the sources above rather than adding to
them: the mechanisms are theirs, the reduction to seven principles is mine, and
anyone who would draw the line elsewhere is not obviously wrong. Section 16 is
mostly practice. "Harness" is ordinary usage in the agent tooling community and
the Ralph material supplies the state-on-disk argument, but the build order, the
ordering of the error-reduction levers and the phase permission table are what
has worked rather than what has been published, and they should be read at that
weight. And section 19 is the one that depends most on a single study, which
has not yet been through peer review.

---

## Open questions for the next revision

- Verify every citation above. Inherited citations are how errors propagate, and
  the Piskala entry now contains two worked examples of it. In particular, read
  METR, DORA and Pearce in the original before section 19 cites them as if we
  had.
- The tool comparison is gone, as of revision 0.4. It was the section that
  would age fastest, Böckeler's hands-on findings had already started
  contradicting parts of it, and a guide that ages badly in one section gets
  distrusted in all of them. What was worth keeping from it, the constitution as
  an example of a tool arriving with opinions, moved into section 11.
- The legal chapter needs a reader who does this for a living to disagree with
  it. It is written from the engineering side of a conversation that has two
  sides.
- Add one worked example end to end, in full, rather than in fragments. Fontoura
  shows how it is done: five complete specifications for one product, every
  requirement traced to a design decision and to a task with a verification
  command. The points promotion in this guide could get the same treatment in an
  appendix.
- Section 19 answers the previous revision's question about the best argument
  against, and section 3 still treats cost only qualitatively. Spec Kit's own
  comparison, roughly twelve hours of documentation work against fifteen minutes
  of commands, and Scott Logic's "ten times slower" are the figures a cost
  section would have to engage with.
- The constitution question is half answered in section 11: it differs from a
  style guide when a validator executes it. The other half remains, who ratifies
  a change to it and by what procedure.
- Section 17 proposes a new check, refusing to ratify a requirement with no
  origin, and nobody has run it. It is cheap to try on a real repository and
  should be tried before it is recommended with more conviction.
- Section 16 orders the error-reduction levers by return on effort. That
  ordering is a judgement from practice and nothing here measures it. The claim
  that the quality of error messages outranks prompt engineering is the most
  testable assertion in this guide and the most embarrassing one to be wrong
  about.
- Mutation testing is recommended in section 16 as an oracle for the oracles,
  over a subset of files. Nobody here has run it at that scope on a repository
  whose tests were written by an agent, which is exactly the case it is being
  recommended for.
- The guide now has twenty sections and the subtitle promises "short". Sections
  9, 16, 17, 18 and 19 have pushed it well past what it promises. The next
  revision should either drop "short" or drop chapters, and the second is the
  harder decision to make honestly about one's own writing.
- Section 19 will age before any other. Hill is a working paper, SpecMine is a
  dataset somebody will mine soon, and replications of the favourable cases will
  arrive or not. Reread it at every revision.
