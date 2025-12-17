import re
from agent.memory import last_intent, get_modifiers

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)   # remove punctuation
    text = re.sub(r"\s+", " ", text)      # normalize spaces
    return text.strip()

def handle_follow_up(question: str):
    """
    Handles follow-up questions like:
    - top 5
    - give top 10
    - show top 3
    """

    q = normalize(question)

    # Must have a previous intent
    prev_intent = last_intent()
    if not prev_intent:
        return None

    # ----------------------------
    # TOP N detection
    # ----------------------------
    match = re.search(r"(top|give top|show top)\s+(\d+)", q)
    if match:
        limit = int(match.group(2))
        modifiers = get_modifiers() or {}
        modifiers["limit"] = limit
        return prev_intent, modifiers

    return None
