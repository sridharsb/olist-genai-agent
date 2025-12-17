# agent/knowledge.py

import json
import os
import re
from typing import List, Optional

# --------------------------------------------------
# Load knowledge files
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")

with open(os.path.join(KNOWLEDGE_DIR, "glossary.json"), encoding="utf-8") as f:
    GLOSSARY = json.load(f)

with open(os.path.join(KNOWLEDGE_DIR, "product_enrichment.json"), encoding="utf-8") as f:
    PRODUCT_INFO = json.load(f)

# --------------------------------------------------
# Category aliases (PT ↔ EN + business synonyms)
# --------------------------------------------------
CATEGORY_ALIASES = {
    "cama_mesa_banho": [
        "bed bath",
        "bed table bath",
        "home textiles",
        "cama mesa banho",
        "bed and bath",
    ],
    "beleza_saude": [
        "beauty",
        "health",
        "cosmetics",
        "personal care",
        "beleza saude",
    ],
    "moveis_decoracao": [
        "furniture",
        "home decor",
        "decor",
        "moveis decoracao",
    ],
    "eletrodomesticos": [
        "home appliances",
        "appliances",
        "eletrodomesticos",
    ],
    "telefonia": [
        "phones",
        "smartphones",
        "mobile phones",
        "telefonia",
    ],
    "pet_shop": [
        "pet products",
        "pet supplies",
        "pet shop",
    ],
}

ALIAS_TO_CATEGORY = {
    alias: category
    for category, aliases in CATEGORY_ALIASES.items()
    for alias in aliases
}

# --------------------------------------------------
# Normalization utilities
# --------------------------------------------------
def normalize(text: str) -> str:
    """
    Normalizes text for robust matching.
    """
    text = text.lower()
    text = re.sub(r"[_\-]", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# --------------------------------------------------
# Definition & enrichment lookup
# --------------------------------------------------
def lookup_definition(query: str) -> Optional[str]:
    """
    Looks up definitions or category explanations.
    Priority:
    1. Glossary definitions
    2. Alias-based category enrichment
    3. Direct category enrichment
    """
    q_norm = normalize(query)

    # 1️⃣ Glossary terms
    for term, definition in GLOSSARY.items():
        if normalize(term) in q_norm:
            return definition

    # 2️⃣ Alias → category enrichment
    for alias, category in ALIAS_TO_CATEGORY.items():
        if normalize(alias) in q_norm:
            return PRODUCT_INFO.get(category)

    # 3️⃣ Direct category match
    for category, explanation in PRODUCT_INFO.items():
        if normalize(category) in q_norm:
            return explanation

    return None


# --------------------------------------------------
# Translation utility (explicit)
# --------------------------------------------------
def translate_category(text: str) -> Optional[str]:
    """
    Translates English aliases to Portuguese category names
    using CONTAINMENT matching.
    """
    q_norm = normalize(text)

    for alias, category in ALIAS_TO_CATEGORY.items():
        if normalize(alias) in q_norm:
            return category

    return None



# --------------------------------------------------
# Contextual insight helper (KEY UPGRADE)
# --------------------------------------------------
def get_category_context(categories: List[str], max_items: int = 3) -> str:
    """
    Returns enriched business context for categories.
    Used for AI explanations and 'why' insights.
    """
    insights = []

    for cat in categories[:max_items]:
        if cat in PRODUCT_INFO:
            insights.append(
                f"- **{cat.replace('_',' ').title()}**: {PRODUCT_INFO[cat]}"
            )

    if not insights:
        return "No additional category context available."

    return "\n".join(insights)


# --------------------------------------------------
# High-level helper (for explainers)
# --------------------------------------------------
def build_explanation_context(df) -> str:
    """
    Builds a reusable context block for explanations
    using structured data + knowledge enrichment.
    """
    if "category" not in df.columns:
        return ""

    categories = df["category"].head(3).tolist()
    return get_category_context(categories)
