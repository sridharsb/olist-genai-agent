import re
from agent.knowledge import lookup_definition

ANALYTICAL_TRIGGERS = [
    "which", "show", "top", "total", "trend",
    "compare", "highest", "lowest", "average"
]

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def handle_conversation(question: str):
    q = normalize(question)

    # --- Metric definitions (explicit, correct) ---
    if "customer lifetime value" in q or "clv" in q:
        return (
            "Customer Lifetime Value (CLV) represents the total revenue "
            "a customer is expected to generate over their entire relationship "
            "with the business."
        )

    # --- Knowledge lookup (only if non-analytical) ---
    if not any(w in q for w in ANALYTICAL_TRIGGERS):
        definition = lookup_definition(q)
        if definition:
            return definition

    # --- Greetings ---
    if q in ["hi", "hello", "hey", "good morning", "good evening"]:
        return "Hello 👋 I’m your Olist e-commerce analytics assistant."

    # --- Small talk ---
    if q in ["how are you", "how are you doing"]:
        return "I’m doing great 😊 Ready to help you explore the Olist e-commerce data."

    # --- Identity ---
    if q in ["what is your name", "who are you"]:
        return (
            "I’m an AI-powered analytics assistant built to help you "
            "analyze and understand the Brazilian Olist e-commerce dataset."
        )

    # --- Help ---
    if "help" in q or "what can you do" in q:
        return (
            "I can analyze the Brazilian Olist e-commerce dataset.\n\n"
            "Examples:\n"
            "- Show revenue by category\n"
            "- Highest revenue category\n"
            "- Average order value by category\n"
            "- Top 5 categories\n"
        )

    return None
