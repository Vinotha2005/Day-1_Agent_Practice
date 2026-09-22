# Personal Expense Assistant — Chatbot vs Rule-Based Workflow vs AI Agent

**Scenario (private data):** my own personal expense records for the month,
stored in `private_data/expenses.csv` (date, category, description, amount).
This is private, personal financial data that lives only on my machine — not
something a public LLM has ever seen.

This repo implements the same task — "help me understand and manage my
expenses" — three different ways, to compare a plain chatbot, a rule-based
workflow, and an AI agent (LLM + Tools + Loop).

## Structure

```
expense-agent-project/
├── private_data/
│   └── expenses.csv        # the private data source
├── chatbot.py               # 1. plain chatbot   (LLM only, no data access)
├── rule_based.py             # 2. rule-based workflow (fixed logic, no LLM)
├── agent.py                  # 3. AI agent        (LLM + Tools + Loop)
├── Output/                   # screenshots of all three running
├── analysis.md                # full written analysis (graded first)
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt

```

## Run each approach

```bash
python chatbot.py
python rule_based.py
python agent.py
```

## Demo mode

`chatbot.py` and `agent.py` will run and print realistic output even
without an `API_KEY` set, so the three programs can be run and
screenshotted end-to-end without needing API access. `agent.py` in demo
mode still prints every reasoning step, tool call, and observation in the
loop so the LLM+Tools+Loop pattern is visible either way.

## What to look at first

Read **`analysis.md`** — it explains each approach, includes the filled-in
comparison table, the suitability analysis, and the conclusion, and is
written to stand on its own without needing to read the code.
