"""
============================================================
🧪 FINAL AGENT TEST SUITE (LEGACY + NEW SCENARIOS)
============================================================
Covers:
- Conversation
- Knowledge lookups
- Revenue analytics
- AOV analytics
- Follow-ups
- Translation & enrichment
- Insight generation
- Safety
============================================================
"""

import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from agent.agent_core import answer
from agent.memory import reset_memory


# ----------------------------------------------------------
# Helpers
# ----------------------------------------------------------
def assert_metric(df, metric):
    cols = set(c.lower() for c in df.columns)

    if metric == "revenue":
        assert "revenue" in cols, f"Expected revenue column, got {cols}"
        assert "average_order_value" not in cols, "AOV leaked into revenue result"

    elif metric == "aov":
        assert "average_order_value" in cols, f"Expected AOV column, got {cols}"
        assert "revenue" not in cols, "Revenue leaked into AOV result"


def run_test(
    name,
    question,
    expect_type="data",
    metric=None,
    min_rows=None,
    exact_rows=None,
    expect_insight=False,
    reset=True,
):
    if reset:
        reset_memory()

    print("\n" + "=" * 60)
    print(f"🧪 TEST: {name}")
    print(f"Q: {question}")
    print("=" * 60)

    result = answer(question)

    # ------------------------------
    # Text response
    # ------------------------------
    if expect_type == "text":
        assert isinstance(result, str), f"Expected text, got {type(result)}"
        print("✔ Text response")
        print(result)
        print("✅ PASS")
        return

    # ------------------------------
    # Data response
    # ------------------------------
    assert isinstance(result, dict), f"Expected dict, got {type(result)}"
    df = result.get("df")

    assert df is not None, "Missing DataFrame in result"
    print(f"✔ DataFrame returned ({len(df)} rows)")
    print("↳ Columns:", list(df.columns))
    print(df.head())

    if metric:
        assert_metric(df, metric)
        print(f"✔ Metric check ({metric})")

    if min_rows is not None:
        assert len(df) >= min_rows, f"Expected ≥ {min_rows} rows"

    if exact_rows is not None:
        assert len(df) == exact_rows, f"Expected exactly {exact_rows} rows"

    if expect_insight:
        assert result.get("insight"), "Expected insight but none returned"
        print("✔ Insight generated")

    print("✅ PASS")


# ----------------------------------------------------------
# Test Runner
# ----------------------------------------------------------
def main():
    print("\n==============================")
    print("🚀 RUNNING FINAL AGENT TEST SUITE")
    print("==============================")

    # ------------------------------
    # Conversation
    # ------------------------------
    run_test("Greeting", "HELLO!!!", expect_type="text")
    run_test("Identity", "what is your name ?", expect_type="text")
    run_test("Small talk", "how are you?", expect_type="text")

    # ------------------------------
    # Knowledge & translation
    # ------------------------------
    run_test(
        "Category definition (PT)",
        "what is cama mesa banho ?",
        expect_type="text",
    )

    run_test(
        "Category definition (EN alias)",
        "what are bed bath products?",
        expect_type="text",
    )

    run_test(
        "Metric definition (CLV)",
        "define customer lifetime value",
        expect_type="text",
    )

    # ------------------------------
    # Revenue analytics
    # ------------------------------
    reset_memory()
    run_test(
        "Revenue by category",
        "show revenue by category",
        metric="revenue",
        min_rows=5,
        expect_insight=True,
        reset=False,
    )

    run_test(
        "Revenue follow-up top 3",
        "top 3",
        metric="revenue",
        exact_rows=3,
        reset=False,
    )

    run_test(
        "Filtered revenue (category alias)",
        "show revenue for bed bath",
        metric="revenue",
        exact_rows=1,
        reset=True,
    )

    # ------------------------------
    # AOV analytics (category-level)
    # ------------------------------
    reset_memory()
    run_test(
        "AOV by category",
        "average order value by category",
        metric="aov",
        min_rows=5,
        reset=False,
    )

    run_test(
        "AOV by category follow-up top 3",
        "top 3",
        metric="aov",
        exact_rows=3,
        reset=False,
    )

    # ------------------------------
    # AOV analytics (global)
    # ------------------------------
    reset_memory()
    run_test(
        "Global AOV",
        "what is average order value",
        metric="aov",
        exact_rows=1,
        reset=False,
    )

    run_test(
        "Global AOV follow-up (safe)",
        "top 3",
        metric="aov",
        exact_rows=1,
        reset=False,
    )

    # ------------------------------
    # Safety & robustness
    # ------------------------------
    run_test(
        "Follow-up without context",
        "give top 5",
        expect_type="text",
    )

    run_test(
        "Unsupported analysis",
        "predict revenue next year",
        expect_type="text",
    )

    run_test(
        "Garbage input",
        "asdfghjkl",
        expect_type="text",
    )

    run_test(
        "SQL injection attempt",
        "drop table orders;",
        expect_type="text",
    )

    print("\n🎉 ALL FINAL TESTS PASSED SUCCESSFULLY")
    print("===============================")


if __name__ == "__main__":
    main()
