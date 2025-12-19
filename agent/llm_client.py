from openai import OpenAI, APIConnectionError

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="lm-studio"
)

MODEL = "qwen2.5-7b-instruct"

def llm_generate(prompt: str):
    """
    Generate AI explanation text.
    - Handles connection errors gracefully
    - Used only on-demand via UI button
    - Result is cached at Streamlit level
    """

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300,
            timeout=30.0  # 30 second timeout for explanations
        )
        return resp.choices[0].message.content.strip()

    except APIConnectionError:
        return (
            "⚠️ LLM service unavailable. "
            "To enable AI explanations, start LM Studio on port 8000. "
            "The data result above is still accurate."
        )
    except Exception as e:
        return (
            "⚠️ Unable to generate AI explanation at the moment. "
            "The data result above is still accurate."
        )
