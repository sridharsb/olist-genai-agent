from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="lm-studio"
)

MODEL = "qwen2.5-7b-instruct"

def llm_detect_intent(question: str, allowed_intents: list):

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
        max_tokens=20
    )

    intent = resp.choices[0].message.content.strip().lower()
    intent = intent.replace("`", "").replace('"', "")

    if intent == "none":
        return None

    return intent if intent in allowed_intents else None
