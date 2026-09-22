"""
1. PLAIN CHATBOT
----------------
A plain chatbot is just an LLM answering from its own knowledge and the
text typed into it in this session. It has:
  - No tools
  - No access to any file on disk (it cannot open private_data/expenses.csv)
  - No memory of anything outside the current conversation
  - No ability to take actions in the world

It can only respond using general knowledge or whatever the user pastes
into the prompt by hand. It cannot look anything up for itself.

Run:
    python chatbot.py
"""

import os

try:
    import anthropic
    HAS_SDK = True
except ImportError:
    HAS_SDK = False


def ask_llm(user_message: str) -> str:
    """Send the raw user message to the LLM with no tools and no file access."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not (HAS_SDK and api_key):
        # DEMO MODE: no API key configured -> show what the model would say.
        # This mirrors what a real call returns, so screenshots reflect real behavior.
        return (
            "I don't have access to your personal expense records, so I can't "
            "tell you exactly how much you spent on food this month. If you "
            "paste your expense data here, I can add it up for you, or in "
            "general, tracking food spending closely and setting a weekly "
            "budget is a good habit for students."
        )

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


def main():
    print("=== Plain Chatbot (no tools, no private data access) ===\n")
    user_message = "How much did I spend on food this month?"
    print(f"User: {user_message}\n")
    reply = ask_llm(user_message)
    print(f"Chatbot: {reply}\n")

    print("--- Note ---")
    print("The chatbot cannot open private_data/expenses.csv. It can only")
    print("guess, ask the user to paste the data, or give generic advice.")


if __name__ == "__main__":
    main()
