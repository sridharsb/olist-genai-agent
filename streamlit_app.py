# streamlit_app.py - Enhanced Olist Analytics Assistant

import sys
import os
import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional

# --------------------------------------------------
# Path setup
# --------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
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
# Custom CSS for colorful, modern UI
# --------------------------------------------------
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary: #6366f1;
        --secondary: #8b5cf6;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --info: #3b82f6;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e7ff;
        padding: 0.75rem;
        font-size: 1.1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Success/Info boxes */
    .stSuccess, .stInfo {
        border-radius: 10px;
        border-left: 5px solid;
    }
    
    /* Chart container */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* History items */
    .history-item {
        background: linear-gradient(90deg, #f0f9ff 0%, #e0e7ff 100%);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #6366f1;
        transition: all 0.3s ease;
    }
    
    .history-item:hover {
        transform: translateX(5px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0e7ff 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0 1rem 0;
        border-left: 5px solid #6366f1;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="🛒 Olist Analytics Assistant",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# Header with gradient
# --------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🛒 Olist Analytics Assistant</h1>
    <p style="font-size: 1.2rem; margin-top: 0.5rem; opacity: 0.9;">
        Conversational analytics on Brazilian e-commerce data (2016–2018)
    </p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Session state initialization
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
# Helper functions
# --------------------------------------------------
def prettify_df(df: pd.DataFrame) -> pd.DataFrame:
    """Format DataFrame for better display."""
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


def format_currency(value: float) -> str:
    """Format currency values."""
    return f"R$ {value:,.2f}"


def show_kpis(df: pd.DataFrame) -> None:
    """Display colorful KPI cards."""
    st.markdown('<div class="section-header"><h2>📌 Key Highlights</h2></div>', unsafe_allow_html=True)
    
    cols = st.columns(3)

    if "revenue" in df.columns:
        total_revenue = df['revenue'].sum()
        top_category = df.iloc[0]["category"] if len(df) > 0 else "N/A"
        highest_revenue = df.iloc[0]['revenue'] if len(df) > 0 else 0
        
        cols[0].metric(
            "💰 Total Revenue",
            format_currency(total_revenue),
            delta=None
        )
        cols[1].metric(
            "🏆 Top Category",
            top_category,
            delta=None
        )
        cols[2].metric(
            "📈 Highest Revenue",
            format_currency(highest_revenue),
            delta=None
        )

    elif "average_order_value" in df.columns:
        aov = df.iloc[0]['average_order_value'] if len(df) > 0 else 0
        num_categories = len(df)
        
        cols[0].metric(
            "📦 Avg Order Value",
            format_currency(aov),
            delta=None
        )
        cols[1].metric(
            "🗂 Categories Shown",
            num_categories,
            delta=None
        )
        cols[2].metric(
            "🔍 Scope",
            "Category-level",
            delta=None
        )
    
    elif "units_sold" in df.columns:
        total_units = df['units_sold'].sum()
        top_category = df.iloc[0]["category"] if len(df) > 0 else "N/A"
        top_units = df.iloc[0]['units_sold'] if len(df) > 0 else 0
        
        cols[0].metric(
            "📦 Total Units Sold",
            f"{total_units:,}",
            delta=None
        )
        cols[1].metric(
            "🏆 Top Category",
            top_category,
            delta=None
        )
        cols[2].metric(
            "📈 Highest Units",
            f"{top_units:,}",
            delta=None
        )


def render_chart(df: pd.DataFrame, x_col: str, y_col: str) -> None:
    """Render styled chart."""
    with st.container():
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        try:
            fig = plot(df, x_col, y_col)
            st.pyplot(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error rendering chart: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# Main input section
# --------------------------------------------------
st.markdown("### 💬 Ask Your Question")
q = st.text_input(
    "Question",
    placeholder="e.g. Which category has the highest revenue?",
    label_visibility="collapsed",
    key="question_input"
)

# --------------------------------------------------
# Main logic
# --------------------------------------------------
if q:
    st.session_state.history.insert(0, q)

    # Avoid recomputation on UI toggles
    if q != st.session_state.last_question:
        with st.spinner("🔍 Analyzing your question..."):
            result = answer(q)
        st.session_state.last_result = result
        st.session_state.last_question = q
    else:
        result = st.session_state.last_result

    # --------------------------------------------------
    # Text response (error messages)
    # --------------------------------------------------
    if isinstance(result, str):
        st.error(f"⚠️ {result}")

    # --------------------------------------------------
    # Data response
    # --------------------------------------------------
    else:
        df = prettify_df(result["df"])

        # Header with gradient styling
        st.markdown("""
        <div class="section-header">
            <h2>📊 Analysis Result</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Summary
        if result.get("summary"):
            st.markdown(result["summary"])

        # KPI cards
        show_kpis(df)

        st.markdown("---")

        # View toggle with better styling
        col1, col2 = st.columns([1, 4])
        with col1:
            view = st.radio(
                "📊 View as",
                ["📋 Table", "📈 Chart"],
                horizontal=True,
                key="view_toggle"
            )

        # Display based on selection
        if view == "📋 Table":
            st.markdown("### 📋 Data Table")
            st.dataframe(
                df,
                use_container_width=True,
                height=400
            )
        else:
            st.markdown("### 📈 Visual Chart")
            if len(df.columns) >= 2:
                render_chart(df, df.columns[0], df.columns[1])
            else:
                st.warning("Not enough columns to create a chart.")

        # Download button
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            st.download_button(
                "📥 Download CSV",
                df.to_csv(index=False),
                "olist_analysis_result.csv",
                "text/csv",
                key="download_csv",
                use_container_width=True
            )

        # Category knowledge
        if "category" in df.columns:
            categories = (
                df["category"]
                .str.replace(" ", "_")
                .str.lower()
                .unique()
                .tolist()
            )
            if categories:
                with st.expander("📦 About the Categories", expanded=False):
                    context = get_category_context(categories)
                    if context:
                        st.info(context)
                    else:
                        st.info("No additional context available for these categories.")

        # Fast insight
        if result.get("insight"):
            st.success(result["insight"])

        st.markdown("---")

        # AI Explanation section
        st.markdown("""
        <div class="section-header">
            <h2>🤖 AI Explanation</h2>
        </div>
        """, unsafe_allow_html=True)
        
        explain_col1, explain_col2 = st.columns([1, 3])
        with explain_col1:
            explain_clicked = st.button(
                "🧠 Generate AI Explanation",
                use_container_width=True,
                key="explain_button"
            )

        if explain_clicked:
            if q not in st.session_state.explanations:
                with st.spinner("🤖 Generating AI-powered explanation..."):
                    try:
                        st.session_state.explanations[q] = explain(q, df)
                    except Exception as e:
                        st.session_state.explanations[q] = (
                            f"⚠️ Unable to generate explanation: {str(e)}"
                        )

        if q in st.session_state.explanations:
            st.markdown("---")
            explanation = st.session_state.explanations[q]
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f0f9ff 0%, #e0e7ff 100%);
                padding: 1.5rem;
                border-radius: 10px;
                border-left: 5px solid #6366f1;
                margin: 1rem 0;
            ">
                <p style="margin: 0; line-height: 1.8; font-size: 1.05rem;">
                    {explanation}
                </p>
            </div>
            """, unsafe_allow_html=True)

# --------------------------------------------------
# Conversation history sidebar
# --------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    ">
        <h2>🕘 History</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.history:
        for i, h in enumerate(st.session_state.history[:10]):
            st.markdown(f"""
            <div class="history-item">
                <strong>Q{i+1}:</strong> {h}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No queries yet. Ask a question to get started!")
