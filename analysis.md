# Analysis: Chatbot vs Rule-Based Workflow vs AI Agent
### Scenario: Personal Expense Assistant (private expense records)

## Scenario Description

The private-data scenario I chose is my own personal expense tracking. I keep
a record of my daily spending — date, category (Food, Travel, Stationery,
Entertainment), description, and amount — in a private file,
`private_data/expenses.csv`. This is private data in the truest sense: it is
personal financial information that lives only on my own machine and has
never been seen by any public model. The task I want solved is simple to
describe but genuinely useful: "help me understand and manage my spending,"
covering requests like knowing my category totals, my overall spending, and
comparisons between categories. I implemented this same task three times —
once as a plain chatbot, once as a rule-based workflow, and once as an AI
agent — to compare how each approach behaves on identical private data and
identical user requests.

## 1. Explanation of Each Approach

### 1.1 Plain Chatbot (`chatbot.py`)

A plain chatbot is an LLM and nothing else. It has no tools, no file access,
and no way to look anything up; it can only respond using its own trained
knowledge plus whatever text is typed directly into the prompt. In this
project, when I ask the chatbot "How much did I spend on food this month?",
it cannot open `expenses.csv` at all — that file simply does not exist from
its point of view. The best it can do is admit it has no access to my
records, ask me to paste the numbers in myself, or fall back on generic
advice about budgeting. Its request-handling is a single round trip: the user
types a message, the LLM generates one response from that message alone, and
the interaction ends. There is no notion of "go check something first." The
limitation on this scenario is severe and structural: the chatbot cannot ever
give me an actually correct number, because it has no private-data access of
any kind — not a partial or read-only kind, but none.

### 1.2 Rule-Based Workflow (`rule_based.py`)

A rule-based workflow is the opposite kind of system: it involves no LLM at
all, only a fixed sequence of `if / elif` conditions that a programmer wrote
in advance. Because I, as the developer, hard-coded the exact file path and
exact column names of `expenses.csv` into the script, this workflow *can*
read the private data directly — it opens the CSV, sums the `amount` column,
and applies whatever logic I specified. This is genuinely more useful than
the chatbot for the handful of things I anticipated: "total for a known
category," "overall total," and "number of transactions" all work reliably
and deterministically, because they are exactly the branches I coded. The
moment a request falls outside those exact patterns — for example, "predict
my spending for next month" or "how much more did I spend on Travel than
Entertainment" — the workflow has no branch for it and returns a fixed
fallback message. It requires zero reasoning and zero understanding of
language; it is pure pattern-matching against keywords I chose ahead of
time, so its ceiling is exactly the set of situations I imagined while
writing it.

### 1.3 AI Agent (`agent.py`)

The agent combines all three ingredients — **LLM + Tools + Loop**. The LLM
is given a small toolbox (`read_expenses`, `filter_by_category`,
`sum_amount`, `add_expense`) and, critically, is *not* told which tool to
call for which request. When I give it "How much more did I spend on Travel
than Entertainment this month?" — a comparison I never explicitly coded for
anywhere — the agent reasons that it needs two category totals, calls
`filter_by_category("Travel")`, observes the result, calls
`filter_by_category("Entertainment")`, observes that result, and only then
computes the difference and answers. This reason → act → observe → repeat
cycle is the "loop": the agent keeps taking actions and looking at what came
back until it decides it has enough to finish, rather than stopping after
one fixed step like the workflow or one fixed generation like the chatbot.
Because the agent has genuine tool access to the private file (through
functions I still had to write and expose, exactly like the workflow), it
gets a correct, grounded answer instead of the chatbot's guess. Its
limitation on this scenario is different in kind from the other two: it is
not that it *can't* handle novel phrasing, but that its correctness depends
on the tools it's given being well-defined and safe (e.g. `add_expense`
really does modify my private file, so a careless agent could act on a
misread instruction), and that each reasoning + tool-call round trip costs
more time and money than the workflow's instant lookup.

## 2. Comparison Table

| Basis for comparison | Plain chatbot | Rule-based workflow | AI agent |
|---|---|---|---|
| **Flexibility** | High-sounding but hollow — it can respond to any phrasing, but never with real data, so answers are generic regardless of wording. | Very low — only the exact patterns coded in advance work; anything else hits the fallback message. | High — handles novel requests (e.g. category comparisons) it was never explicitly programmed for, by combining tools it already has. |
| **Decision-making** | None — one LLM generation per message, no branching logic. | Fixed and deterministic — the same input always triggers the same pre-written branch. | Dynamic — the LLM decides which tool(s) to call, in what order, based on the specific request. |
| **Tool usage** | None. | None (direct file access hard-coded by the programmer, not "tool use" in the agentic sense). | Explicit, LLM-selected tools (`read_expenses`, `filter_by_category`, `sum_amount`, `add_expense`). |
| **Private-data access** | None — cannot open `expenses.csv` under any circumstance. | Yes, but only through the exact operations the programmer anticipated. | Yes, and flexibly — the agent can combine tools to answer questions the programmer didn't foresee. |
| **Multi-step task handling** | None — single request, single response. | None — one rule fires per request; no chaining between steps. | Yes — the loop lets it chain multiple tool calls (filter Travel → filter Entertainment → subtract) to answer one compound question. |
| **Automation** | Low — essentially a text generator; a human still has to do everything else. | Medium — automates the specific lookups it was coded for, with no human needed for those. | High — can automate multi-step tasks end-to-end, including actions like adding a new expense via `add_expense`. |
| **Reliability** | Low on factual questions about private data — confidently vague or simply wrong, since it's guessing. | Very high, but only within its coded scope; perfectly reliable for known patterns, completely unable outside them. | Generally high and grounded (numbers come from the real file via tools), but slightly less predictable than the workflow since the LLM's tool-choice reasoning can occasionally go a different route than expected. |

## 3. Suitability Analysis

For my expense-tracking scenario, the **AI agent is the most suitable
approach**. The core requirement of this task is twofold: the assistant
must have real access to my private data, and it must be able to answer
questions I did not specifically anticipate when I built it — spending
comparisons, running totals, category breakdowns, and eventually actions
like logging a new expense, all in natural language. The plain chatbot fails
the very first requirement (private-data access is entirely absent from
its comparison-table row), so it is disqualified regardless of how
flexible its language is. The rule-based workflow does satisfy
private-data access and is in fact the most reliable *within its scope* —
if my only need were ever "give me the Food total," the workflow would be
the cheaper, faster, and more predictable choice, since it needs no LLM
call at all. But personal finance questions are naturally varied ("how much
more on X than Y," "what did I spend most on," "add this new expense"), and
the workflow's reliability collapses the instant a question falls outside
its hard-coded branches, which happens often in practice. The agent's
combination of real private-data access (via tools) with the flexibility
and multi-step reasoning to handle whatever phrasing I actually use is
exactly what the comparison table shows it to be uniquely good at, which is
why it is the best fit here.

## 4. Conclusion

Looking beyond this one scenario, the three approaches suit different kinds
of problems because each row of the comparison table reflects a real
underlying trade-off. A **plain chatbot** is the right choice when the task
is genuinely just about language — brainstorming, explaining a concept,
drafting text, or answering general-knowledge questions — where no private
data or real-world action is required, and where the low cost and
simplicity of "just ask an LLM" outweighs the lack of tools or memory. A
**rule-based workflow** is the right choice when the set of possible
requests is small, well-known in advance, and needs to behave with
perfect, auditable predictability — think of a form that always validates
input the same way, or a system triggering a fixed alert when a sensor
value crosses a threshold; here, the workflow's very inflexibility is a
feature, because reliability and speed matter more than adapting to novel
phrasing, and there is no LLM cost or unpredictability at all. An **AI
agent** is the right choice precisely when a task needs both real access to
data or systems (private files, APIs, databases) *and* the flexibility to
handle requests that cannot all be enumerated ahead of time, especially
when the task naturally breaks into multiple steps that depend on each
other's results, as my expense-comparison example does. In short: choose a
chatbot when you only need words, a rule-based workflow when you need
guaranteed behavior over a known, narrow set of cases, and an agent when
you need grounded, multi-step reasoning over real data and actions whose
exact shape you can't fully predict in advance.
