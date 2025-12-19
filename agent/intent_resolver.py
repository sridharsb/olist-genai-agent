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
    q_words = set(re.findall(r"\b\w+\b", q))

    # ----------------------------------
    # 1️⃣ Detect metric explicitly
    # ----------------------------------
    detected_metric = None
    for metric, keywords in METRIC_PRIORITY.items():
        if any(k in q for k in keywords):
            detected_metric = metric
            break

    # ----------------------------------
    # 2️⃣ Match intents that contain the metric
    # ----------------------------------
    if detected_metric:
        # Look for intents that contain the metric in their name
        for intent, phrases in INTENT_SYNONYMS.items():
            if detected_metric not in intent:
                continue

            # Check if all key words from phrase are in the question
            for phrase in phrases:
                phrase_words = set(phrase.split())
                # Check if all phrase words are present in question
                if phrase_words.issubset(q_words) or phrase in q:
                    return intent

    # ----------------------------------
    # 3️⃣ Fallback to normal matching (flexible word order)
    # ----------------------------------
    for intent, phrases in INTENT_SYNONYMS.items():
        for phrase in phrases:
            phrase_words = phrase.split()

            if len(phrase_words) == 1:
                if phrase_words[0] in q_words:
                    return intent
            else:
                # Check exact phrase match first
                if phrase in q:
                    return intent
                # Then check if all words from phrase are in question (flexible order)
                phrase_word_set = set(phrase_words)
                if phrase_word_set.issubset(q_words) and len(phrase_word_set) >= 2:
                    return intent

    return None
