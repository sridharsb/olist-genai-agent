import re
from agent.intent_map import INTENT_SYNONYMS

# Explicit metric keywords → intent roots
METRIC_PRIORITY = {
    "revenue": ["revenue"],
    "average_order_value": ["average", "aov", "order value"],
    "units": ["units", "sold"],
}

def detect_intent(question: str):
    q = question.lower().strip()

    # ----------------------------------
    # 1️⃣ Detect metric explicitly
    # ----------------------------------
    detected_metric = None
    for metric, keywords in METRIC_PRIORITY.items():
        if any(k in q for k in keywords):
            detected_metric = metric
            break

    # ----------------------------------
    # 2️⃣ Prefer intents matching metric
    # ----------------------------------
    if detected_metric:
        for intent, phrases in INTENT_SYNONYMS.items():
            if not intent.startswith(detected_metric):
                continue

            for phrase in phrases:
                if phrase in q:
                    return intent

    # ----------------------------------
    # 3️⃣ Fallback to normal matching
    # ----------------------------------
    words = set(re.findall(r"\b\w+\b", q))

    for intent, phrases in INTENT_SYNONYMS.items():
        for phrase in phrases:
            phrase_words = phrase.split()

            if len(phrase_words) == 1:
                if phrase_words[0] in words:
                    return intent
            else:
                if phrase in q:
                    return intent

    return None
