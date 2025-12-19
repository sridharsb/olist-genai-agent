from openai import OpenAI, APIConnectionError

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="lm-studio"
)

MODEL = "qwen2.5-7b-instruct"

def llm_detect_intent(question: str, allowed_intents: list):
    """
    Attempts to detect intent using LLM.
    Returns None if LLM is unavailable or no match found.
    """
    try:
        prompt = f"""
Choose the BEST matching intent from this list:
{allowed_intents}

User question:
"{question}"

Rules:
- Return ONLY the intent name
- If none match, return NONE
"""

        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=20,
            timeout=5.0  # 5 second timeout
        )

        intent = resp.choices[0].message.content.strip().lower()
        intent = intent.replace("`", "").replace('"', "")

        if intent == "none":
            return None

        return intent if intent in allowed_intents else None
    
    except (APIConnectionError, Exception):
        # LLM service unavailable - silently fall back to rule-based detection
        return None
