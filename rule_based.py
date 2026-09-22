"""
2. RULE-BASED WORKFLOW
-----------------------
A rule-based workflow follows a fixed, predefined set of steps and
conditions. There is NO LLM involved anywhere in this file -- every
branch is an "if / elif" written in advance by the programmer.

It CAN read the private data file directly (because a human wrote the
exact file path and column names into the code), but it can only answer
the specific handful of request patterns it was explicitly coded for.
Anything outside those patterns fails or returns a fixed error message.

Run:
    python rule_based.py
"""

import csv
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "private_data", "expenses.csv")


def load_expenses():
    rows = []
    with open(DATA_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["amount"] = float(row["amount"])
            rows.append(row)
    return rows


def handle_request(user_message: str) -> str:
    """A fixed decision tree. Every branch was hand-written in advance."""
    expenses = load_expenses()
    message = user_message.lower()

    # Rule 1: total spend on a known category
    categories = {"food", "travel", "stationery", "entertainment"}
    for category in categories:
        if category in message and "total" in message or (category in message and "how much" in message):
            total = sum(e["amount"] for e in expenses if e["category"].lower() == category)
            return f"Total spent on {category.title()}: Rs.{total:.2f}"

    # Rule 2: overall total
    if "total" in message and "spend" in message:
        total = sum(e["amount"] for e in expenses)
        return f"Total spending recorded: Rs.{total:.2f}"

    # Rule 3: number of transactions
    if "how many" in message and "transaction" in message:
        return f"Number of recorded transactions: {len(expenses)}"

    # No matching rule -> fixed fallback. A rule-based system cannot improvise.
    return "Sorry, I can only answer: category totals, overall total, or transaction count."


def main():
    print("=== Rule-Based Workflow (fixed logic, no LLM) ===\n")

    test_messages = [
        "How much did I spend on food this month?",
        "What is my total spend?",
        "How many transactions do I have?",
        "Predict my spending for next month",  # outside the fixed rules
    ]

    for msg in test_messages:
        print(f"User: {msg}")
        print(f"Workflow: {handle_request(msg)}\n")


if __name__ == "__main__":
    main()
