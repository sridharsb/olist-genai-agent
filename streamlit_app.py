# agent/streamlit_app.py

import sys
import os
import streamlit as st
import pandas as pd

# --------------------------------------------------
# Path setup
# --------------------------------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# --------------------------------------------------
# Imports
# --------------------------------------------------
from agent.agent_core import answer
from agent.llm_explain import explain
from agent.chart import plot
from agent.knowledge import get_category_context

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="🛒 Olist Analytics Assistant",
    layout="wide",
)

st.title("🛒 Olist Analytics Assistant")
st.caption("Conversational analytics on Brazilian e-commerce data (Olist 2016–2018)")

# --------------------------------------------------
# Session state
# --------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "last_question" not in st.session_state:
    st.session_state.last_question = None

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "explanations" not in st.session_state:
    st.session_state.explanations = {}

# --------------------------------------------------
# Helpers
# --------------------------------------------------
def prettify_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "category" in df.columns:
        df["category"] = (
            df["category"]
            .str.replace("_", " ")
            .str.title()
        )

    if "seller_id" in df.columns:
        df.insert(0, "Seller", [f"Seller #{i+1}" for i in range(len(df))])
        df.drop(columns=["seller_id"], inplace=True)

    if "product_id" in df.columns:
        df.insert(0, "Product", [f"Product #{i+1}" for i in range(len(df))])
        df.drop(columns=["product_id"], inplace=True)

    return df


def show_kpis(df: pd.DataFrame):
    st.markdown("## 📌 Key Highlights")

    cols = st.columns(3)

    if "revenue" in df.columns:
        cols[0].metric(
            "💰 Total Revenue",
            f"R$ {df['revenue'].sum():,.0f}"
        )
        cols[1].metric(
            "🏆 Top Category",
            df.iloc[0]["category"]
        )
        cols[2].metric(
            "📈 Highest Revenue",
            f"R$ {df.iloc[0]['revenue']:,.0f}"
        )

    elif "average_order_value" in df.columns:
        cols[0].metric(
            "📦 Avg Order Value",
            f"R$ {df.iloc[0]['average_order_value']:,.2f}"
        )
        cols[1].metric(
            "🗂 Categories Shown",
            len(df)
        )
        cols[2].metric(
            "🔍 Scope",
            "Category-level"
        )


# --------------------------------------------------
# Input
# --------------------------------------------------
q = st.text_input(
    "Ask a question",
    placeholder="e.g. Which category has the highest revenue?",
)

# --------------------------------------------------
# Main logic
# --------------------------------------------------
if q:
    st.session_state.history.insert(0, q)

    # Avoid recomputation on UI toggles
    if q != st.session_state.last_question:
        result = answer(q)
        st.session_state.last_result = result
        st.session_state.last_question = q
    else:
        result = st.session_state.last_result

    # --------------------------------------------------
    # Text response
    # --------------------------------------------------
    if isinstance(result, str):
        st.warning(result)

    # --------------------------------------------------
    # Data response
    # --------------------------------------------------
    else:
        df = prettify_df(result["df"])

        # -------------------------------
        # Header
        # -------------------------------
        st.markdown("## 📊 Analysis Result")
        st.markdown(result["summary"])

        # -------------------------------
        # KPI cards
        # -------------------------------
        show_kpis(df)

        st.markdown("---")

        # -------------------------------
        # Table / Chart toggle
        # -------------------------------
        view = st.radio(
            "View as",
            ["📋 Table", "📊 Chart"],
            horizontal=True
        )

        if view == "📋 Table":
            st.dataframe(df, use_container_width=True)
        else:
            fig = plot(df, df.columns[0], df.columns[1])
            st.pyplot(fig)

        # -------------------------------
        # Download
        # -------------------------------
        st.download_button(
            "📥 Download CSV",
            df.to_csv(index=False),
            "result.csv",
            "text/csv"
        )

        # -------------------------------
        # Category knowledge
        # -------------------------------
        if "category" in df.columns:
            categories = (
                df["category"]
                .str.replace(" ", "_")
                .str.lower()
                .unique()
                .tolist()
            )
            if categories:
                with st.expander("📦 About the Categories"):
                    context = get_category_context(categories)
                    st.info(context or "No additional context available.")

        # -------------------------------
        # Fast insight (non-LLM)
        # -------------------------------
        if result.get("insight"):
            st.success(result["insight"])

        st.markdown("---")

        # -------------------------------
        # AI Explanation (on-demand)
        # -------------------------------
        st.markdown("## 🤖 AI Explanation")

        if st.button("🧠 Explain this result"):
            if q not in st.session_state.explanations:
                with st.spinner("Generating explanation..."):
                    st.session_state.explanations[q] = explain(q, df)

        if q in st.session_state.explanations:
            st.write(st.session_state.explanations[q])

# --------------------------------------------------
# Conversation history
# --------------------------------------------------
st.markdown("---")
st.markdown("## 🕘 Conversation History")

for h in st.session_state.history[:10]:
    st.markdown(f"• {h}")
