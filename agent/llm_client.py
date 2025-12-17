from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="lm-studio"
)

MODEL = "qwen2.5-7b-instruct"

def llm_generate(prompt: str):
    """
    Generate AI explanation text.
    - No hard timeout (local models need time)
    - Used only on-demand via UI button
    - Result is cached at Streamlit level
    """

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300
        )
        return resp.choices[0].message.content.strip()

    except Exception as e:
        return (
            "⚠️ Unable to generate AI explanation at the moment. "
            "The data result above is still accurate."
        )
