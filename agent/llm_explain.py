from agent.llm_client import llm_generate
from agent.knowledge import get_category_context

def explain(question: str, df):
    """
    Generates an analyst-style explanation.
    - Avoids meaningless statistics for single-row results
    - Uses domain knowledge only for interpretation
    """

    # Preview for grounding
    preview = df.head(5).to_string(index=False)

    # Category enrichment (for "why" reasoning)
    category_context = ""
    if "category" in df.columns:
        categories = df["category"].dropna().unique().tolist()[:3]
        category_context = get_category_context(categories)

    # Decide whether to include comparative reasoning
    include_comparison = df.shape[0] > 1

    # Build explanation intent
    comparison_instruction = ""
    if include_comparison:
        comparison_instruction = (
            "Compare categories where relevant and highlight differences in performance."
        )
    else:
        comparison_instruction = (
            "Focus on interpreting what this single result represents and why it matters."
        )

    prompt = f"""
You are a senior e-commerce data analyst.

User question:
{question}

Query result:
{preview}

Category business context (for interpretation only):
{category_context}

Instructions:
- Base conclusions strictly on the data shown
- Do NOT invent statistics or causes
- Avoid generic filler explanations
- Explain patterns using category characteristics where relevant
- {comparison_instruction}
- Clearly state business implications

Write a concise, professional explanation in 5–7 sentences.
"""

    return llm_generate(prompt)
