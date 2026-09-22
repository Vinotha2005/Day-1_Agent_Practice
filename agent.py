"""
3. AI AGENT  (LLM + Tools + Loop)
-----------------------------------
Unlike the chatbot (LLM alone) and the workflow (fixed rules, no LLM),
the agent combines all three ingredients:

  LLM    -> reasons about what the user is asking and decides what to do
  Tools  -> functions the agent can choose to call: read_expenses,
            filter_by_category, sum_amount, add_expense
  Loop   -> the agent keeps calling tools and observing results until it
            has everything it needs to answer, instead of stopping after
            one fixed step

This means the agent can handle requests nobody explicitly coded for in
advance (e.g. "how much more did I spend on Travel than Entertainment?"),
because it decides for itself which tools to call and in what order.

Run:
    python agent.py
"""

import csv
import json
import os

try:
    import anthropic
    HAS_SDK = True
except ImportError:
    HAS_SDK = False

DATA_FILE = os.path.join(os.path.dirname(__file__), "private_data", "expenses.csv")


# ---------- Tools the agent is allowed to use ----------

def read_expenses():
    with open(DATA_FILE, newline="") as f:
        return list(csv.DictReader(f))


def filter_by_category(category: str):
    return [e for e in read_expenses() if e["category"].lower() == category.lower()]


def sum_amount(rows):
    return sum(float(r["amount"]) for r in rows)


def add_expense(date: str, category: str, description: str, amount: float):
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, category, description, amount])
    return "added"


TOOLS = [
    {
        "name": "read_expenses",
        "description": "Return every expense row from the private expense file.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "filter_by_category",
        "description": "Return only the expense rows matching a given category (e.g. Food, Travel).",
        "input_schema": {
            "type": "object",
            "properties": {"category": {"type": "string"}},
            "required": ["category"],
        },
    },
    {
        "name": "sum_amount",
        "description": "Sum the 'amount' field of a list of expense rows.",
        "input_schema": {
            "type": "object",
            "properties": {"rows": {"type": "array"}},
            "required": ["rows"],
        },
    },
    {
        "name": "add_expense",
        "description": "Append a new expense to the private expense file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {"type": "string"},
                "category": {"type": "string"},
                "description": {"type": "string"},
                "amount": {"type": "number"},
            },
            "required": ["date", "category", "description", "amount"],
        },
    },
]

TOOL_FUNCTIONS = {
    "read_expenses": lambda **kwargs: read_expenses(),
    "filter_by_category": lambda **kwargs: filter_by_category(kwargs["category"]),
    "sum_amount": lambda **kwargs: sum_amount(kwargs["rows"]),
    "add_expense": lambda **kwargs: add_expense(**kwargs),
}


def run_agent_live(user_message: str) -> str:
    """Real ReAct-style loop using the Anthropic API and tool calling."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [{"role": "user", "content": user_message}]

    for _ in range(6):  # loop: keep going until the model stops calling tools
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"  [agent decides to call tool: {block.name}({block.input})]")
                result = TOOL_FUNCTIONS[block.name](**block.input)
                print(f"  [observation: {result}]")
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    }
                )
        messages.append({"role": "user", "content": tool_results})

    return "Reached loop limit without a final answer."


def run_agent_demo(user_message: str) -> str:
    """
    DEMO MODE (no ANTHROPIC_API_KEY set): manually walks through the same
    reason -> act -> observe -> repeat loop so the agent's behavior can
    still be seen and screenshotted without an API key.
    """
    print("  [agent reasons: the user wants a category comparison, I need two totals]")
    print("  [agent decides to call tool: filter_by_category({'category': 'Travel'})]")
    travel_rows = filter_by_category("Travel")
    travel_total = sum_amount(travel_rows)
    print(f"  [observation: {travel_total}]")

    print("  [agent decides to call tool: filter_by_category({'category': 'Entertainment'})]")
    ent_rows = filter_by_category("Entertainment")
    ent_total = sum_amount(ent_rows)
    print(f"  [observation: {ent_total}]")

    print("  [agent reasons: I now have both totals, I can compute the difference]")
    diff = travel_total - ent_total
    return (
        f"You spent Rs.{travel_total:.2f} on Travel and Rs.{ent_total:.2f} on "
        f"Entertainment, so you spent Rs.{diff:.2f} more on Travel."
    )


def main():
    print("=== AI Agent (LLM + Tools + Loop) ===\n")
    user_message = "How much more did I spend on Travel than Entertainment this month?"
    print(f"User: {user_message}\n")

    if HAS_SDK and os.environ.get("ANTHROPIC_API_KEY"):
        answer = run_agent_live(user_message)
    else:
        print("[no ANTHROPIC_API_KEY found -> running in demo mode]\n")
        answer = run_agent_demo(user_message)

    print(f"\nAgent: {answer}")


if __name__ == "__main__":
    main()
