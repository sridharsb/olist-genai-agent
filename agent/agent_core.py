# agent/agent_core.py
"""
Core agent logic for processing queries and generating responses.
"""

import duckdb
import re
from datetime import datetime
from typing import Dict, Any, Optional, Union
from dateutil.relativedelta import relativedelta

from agent.intent_resolver import detect_intent
from agent.conversation import handle_conversation
from agent.memory import (
    remember_intent,
    remember_modifiers,
    last_intent,
)
from agent.sql_templates import SQL_TEMPLATES
from agent.sql_guardrails import validate_sql
from agent.llm_intent import llm_detect_intent
from agent.followups import handle_follow_up
from agent.insights import generate_insight
from agent.knowledge import translate_category

DB_PATH = "db/olist.db"

# ----------------------------------
# Filter support
# ----------------------------------
FILTER_COLUMNS = {
    "year": ["year"],
    "month": ["year_month"],
    "months": ["order_purchase_timestamp"],
    "category": ["category"],
}

METRIC_KEYWORDS = {
    "revenue": ["revenue"],
    "average": ["average", "aov", "order value"],
    "units": ["units", "sold"],
}

# ----------------------------------
# Helpers
# ----------------------------------
def metric_from_question(q: str) -> Optional[str]:
    """Extract metric type from question text."""
    for metric, words in METRIC_KEYWORDS.items():
        if any(w in q for w in words):
            return metric
    return None


def metric_from_intent(intent: str) -> Optional[str]:
    """Extract metric type from intent name."""
    if not intent:
        return None
    return intent.split("_")[0]


def apply_filters(sql: str, filters: dict):
    if not filters:
        return sql

    sql_clean = sql.strip()

    # ----------------------------------
    # 1️⃣ Remove existing LIMIT (if any)
    # ----------------------------------
    sql_clean = re.sub(
        r"\blimit\s+\d+\b",
        "",
        sql_clean,
        flags=re.IGNORECASE
    ).strip()

    # ----------------------------------
    # 2️⃣ Extract ORDER BY (if any)
    # ----------------------------------
    order_by = ""
    m = re.search(r"\border\s+by\s+.+$", sql_clean, re.IGNORECASE)
    if m:
        order_by = m.group()
        sql_clean = sql_clean[: m.start()].strip()

    conditions = []
    sql_lower = sql_clean.lower()

    # ----------------------------------
    # 3️⃣ WHERE conditions
    # ----------------------------------
    for key, value in filters.items():
        if key == "limit":
            continue

        for col in FILTER_COLUMNS.get(key, []):
            if col not in sql_lower:
                continue

            if key == "month":
                conditions.append(f"{col} LIKE '{value}%'")
            elif key == "months":
                cutoff = datetime.now() - relativedelta(months=value)
                conditions.append(
                    f"{col} >= TIMESTAMP '{cutoff.strftime('%Y-%m-%d')}'"
                )
            elif key == "category":
                conditions.append(f"{col} = '{value}'")
            else:
                conditions.append(f"{col} = {int(value)}")

    if conditions:
        if "where" in sql_lower:
            sql_clean += " AND " + " AND ".join(conditions)
        else:
            sql_clean += " WHERE " + " AND ".join(conditions)

    # ----------------------------------
    # 4️⃣ Re-attach ORDER BY
    # ----------------------------------
    if order_by:
        sql_clean += " " + order_by

    # ----------------------------------
    # 5️⃣ Final LIMIT (only once)
    # ----------------------------------
    if "limit" in filters:
        sql_clean += f" LIMIT {int(filters['limit'])}"

    return sql_clean


# ----------------------------------
# Main entry point
# ----------------------------------
def answer(question: str) -> Union[str, Dict[str, Any]]:
    """
    Main entry point for processing user questions.
    
    Args:
        question: User's natural language question
        
    Returns:
        Either a string error message or a dict with:
        - intent: detected intent name
        - df: pandas DataFrame with results
        - summary: text summary
        - insight: optional insight text
    """
    q = question.strip().lower()

    # ---- Safety ----
    if re.search(r"\b(drop|delete|truncate|alter)\b", q):
        return "Unsafe or unsupported query detected."

    if "predict" in q or "forecast" in q:
        return "I can’t predict future outcomes with the current dataset."

    # ---- Conversation / knowledge ----
    convo = handle_conversation(q)
    if convo:
        return convo

    # ---- Metric override detection ----
    explicit_metric = metric_from_question(q)

    # ---- Follow-ups ----
    follow = handle_follow_up(q)
    if follow:
        intent, filters = follow
    else:
        intent = detect_intent(q)
        filters = {}

        if not intent:
            intent = llm_detect_intent(q, list(SQL_TEMPLATES.keys()))

    last = last_intent()

    # Explicit metric always overrides memory
    if explicit_metric:
        if last and metric_from_intent(last) != explicit_metric:
            last = None
            remember_intent(None)
            remember_modifiers({})
            filters = {}

    if not intent:
        intent = last

    if not intent:
        return "Sorry, I couldn’t map this question to a supported analysis."

    if intent not in SQL_TEMPLATES:
        return "This analysis is not supported yet."

    # --------------------------------------------------
    # Category extraction via knowledge aliases
    # --------------------------------------------------
    translated_category = translate_category(q)
    if translated_category:
        filters["category"] = translated_category

    # --------------------------------------------------
    # 🔑 FINAL INTENT CORRECTION (CRITICAL FIX)
    # If metric is requested FOR a specific category,
    # force single-row semantics
    # --------------------------------------------------
    if "category" in filters:
        if intent == "revenue_by_category":
            intent = "highest_revenue_category"
            filters["limit"] = 1

        elif intent == "units_by_category":
            intent = "most_selling_category"
            filters["limit"] = 1

    # ---- Build & execute SQL ----
    try:
        sql = SQL_TEMPLATES[intent]
        sql = apply_filters(sql, filters)
        validate_sql(sql)

        con = duckdb.connect(DB_PATH)
        df = con.execute(sql).fetchdf()
        con.close()

        if df.empty:
            return "No data found for your query. Try adjusting your filters or question."
    except KeyError:
        return f"Intent '{intent}' not found in SQL templates."
    except ValueError as e:
        return f"SQL validation error: {str(e)}"
    except Exception as e:
        return f"Database error: {str(e)}"

    remember_intent(intent)
    remember_modifiers(filters)

    insight = generate_insight(intent, df)

    return {
        "intent": intent,
        "df": df,
        "summary": f"### 📊 {intent.replace('_', ' ').title()}",
        "insight": insight,
    }
