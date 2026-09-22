# My Expense Assistant — Chatbot vs Rule-Based Workflow vs AI Agent

Hey! This little project is my Day 1 task for the Agentic AI course. The
idea is simple: I picked something real from my own life — my personal
expenses — and built the *same* assistant three different ways, so I could
actually feel the difference between a chatbot, a rule-based workflow, and
a true AI agent, instead of just reading about it.

## What's the scenario?

I keep a small CSV of my own spending (`private_data/expenses.csv`) — date,
category, what it was for, and how much I spent. Nothing fancy, just Food,
Travel, Stationery, Entertainment. This is *my* private data — no chatbot
on the internet has ever seen it, and that's exactly the point.

I wanted to ask it things like:
- "How much did I spend on food this month?"
- "Did I spend more on Travel or Entertainment?"
- "Add a new expense for today."

Then I watched how differently each of the three systems handled that.

## The three systems, in plain English

### 1. `chatbot.py` — just an LLM, nothing else
This one's basically ChatGPT with no extra powers. It can talk, but it
**cannot open my expense file**. So when I ask it "how much did I spend on
food," it has no idea — it just apologizes and asks me to type the numbers
in myself. It's honestly a bit useless for this task, and that's exactly
the lesson: a plain chatbot only knows what you type into it.
<img width="500" height="732" alt="01_chatbot" src="https://github.com/user-attachments/assets/d3a00f7e-8926-45dc-8a71-43dfba8f4152" />

### 2. `rule_based.py` — a bunch of hardcoded if/else rules
This one has zero AI in it. It's just plain code I wrote myself that says
"if the user mentions 'food' and 'total', go add up the Food rows." It
*can* read my real CSV file, so it gives correct answers — but only for the
exact questions I thought to code for. Ask it anything slightly different,
like "predict my spending next month," and it just shrugs with a fixed
error message. It's reliable but rigid — like a vending machine, not an
assistant.
<img width="500" height="684" alt="02_rule_based" src="https://github.com/user-attachments/assets/501ed40e-ff2f-46a6-85cc-2b71d973a686" />


### 3. `agent.py` — the real deal: LLM + Tools + a Loop
This is the interesting one. I gave the LLM a small toolbox — functions
like `filter_by_category`, `sum_amount`, `add_expense` — and let it figure
out *by itself* which ones to use and in what order. So when I asked "how
much more did I spend on Travel than Entertainment," it wasn't a question I
pre-coded anywhere. The agent reasoned it out: grab the Travel total, grab
the Entertainment total, subtract, answer. It kept looping — call a tool,
look at the result, decide the next step — until it actually had the
answer. That loop is the whole magic of an "agent" vs a regular script.
<img width="500" height="948" alt="03_agent" src="https://github.com/user-attachments/assets/3972c931-f3d9-475e-94ad-fb6ca8021ba1" />


## Folder structure

```
expense-agent-project/
├── private_data/
│   └── expenses.csv        <- my sample expense data
├── chatbot.py               <- system 1: LLM only
├── rule_based.py             <- system 2: fixed rules, no LLM
├── agent.py                  <- system 3: LLM + tools + loop
├── Output/                   <- screenshots of all three running
├── analysis.md                <- the full write-up (read this first!)
├── requirements.txt
└── README.md                  <- you are here
```

## How to actually run it

```bash
pip install -r requirements.txt

# optional — only needed for real LLM calls
export API_KEY="your-key-here"

python chatbot.py
python rule_based.py
python agent.py
```

No API key handy? No problem — `chatbot.py` and `agent.py` both have a
built-in "demo mode" that still runs and prints realistic output (including
every reasoning step and tool call the agent makes) so you can try them and
take screenshots without needing to set anything up.

## What I'd actually read first

Honestly, skip the code and go straight to **`analysis.md`**. That's where
I explain each approach in plain language, compare all three side-by-side
in a table, and explain why the agent turned out to be the best fit for a
task like this — plus when I'd actually reach for a chatbot or a rule-based
workflow instead, in general.

## The one-line takeaway

- **Chatbot** = can talk, can't *do* anything.
- **Rule-based workflow** = can do exactly what it was told, nothing more.
- **AI agent** = can figure out *how* to do something it wasn't explicitly
  told how to do, by reasoning and using tools in a loop.
