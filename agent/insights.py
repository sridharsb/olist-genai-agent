# agent/insights.py

CATEGORY_INSIGHTS = {
    "cama_mesa_banho": [
        "Broad product range covering daily essentials",
        "High repeat purchase frequency",
        "Strong seasonal demand",
        "Competitive pricing on Olist"
    ],
    "beleza_saude": [
        "High repeat consumption products",
        "Strong brand loyalty",
        "Health and wellness demand growth"
    ]
}

def generate_insight(intent: str, df):
    if "category" not in df.columns:
        return None

    top_category = df.iloc[0]["category"]

    reasons = CATEGORY_INSIGHTS.get(top_category)
    if not reasons:
        return None

    bullets = "\n".join([f"- {r}" for r in reasons])

    return f"""
### 💡 Why this category performs well

**{top_category.replace('_',' ').title()}**

{bullets}
"""
