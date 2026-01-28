# 🛒 Olist GenAI Analytics Assistant

Demo Video (Google Drive):
https://drive.google.com/file/d/1adJLjPKFtWsXlq9eZPSIkOedSYjLidWC/view?usp=sharing

A conversational GenAI-powered analytics agent for exploring the Brazilian **Olist e‑commerce dataset** using natural language.

> User: Ask business questions in plain English → get **SQL-backed answers, charts, and explanations**.

---

## 🎯 What Problem Does This Solve?
E‑commerce datasets are powerful but inaccessible to non‑technical users.
This project enables **business-friendly analytics without SQL**, supporting follow-ups, explanations, and safe querying.

Example questions:
- "Which category has the highest revenue?"
- "Show revenue by category → top 3"
- "What is *cama mesa banho*?"
- "Average order value by category"

---

## 🚀 Key Capabilities

### 🧠 Agentic Intelligence
- Hybrid **rule-based + LLM** intent detection
- Conversational memory for follow-ups ("top 5", "same for 2018")
- Strict SQL safety guardrails (view-only, no mutations)

### 📊 Analytics Engine
- DuckDB over curated analytical views
- Revenue, AOV, CLV, units sold, customer & seller insights
- Deterministic, fast SQL execution

### 📚 Knowledge Enrichment
- Category explanations (Portuguese ↔ English)
- Metric definitions (AOV, CLV, revenue)
- Business context beyond raw numbers

### 🎨 Streamlit UI
- Chat-based interface
- KPI cards, tables, charts
- Explain-on-demand insights
- Graceful handling of unsupported or unsafe queries

---

## 🧩 High-Level Architecture

User → Streamlit UI → Conversation Router → Agent Core

Agent Core:
- Intent detection (rules + LLM fallback)
- Memory & follow-up resolution
- Knowledge lookup & category aliasing

Agent Core → SQL Builder (guarded) → DuckDB → Results → Insights → UI


---

## 🛠 Tech Stack

| Layer | Technology |
|------|-----------|
| UI | Streamlit |
| Database | DuckDB |
| Data | Olist Brazilian E‑commerce |
| LLM | Local (LM Studio / Ollama) or Gemini |
| Charts | Matplotlib |
| Testing | Custom test harness |

---

## 🤖 LLM Setup

### Option 1: Local LLM (Default)
- LM Studio / Ollama
- Models: Qwen, LLaMA, Mistral
- No API keys, offline-friendly

### Option 2: Cloud LLM
- Google Gemini
- OpenRouter / OpenAI‑compatible APIs

🔧 **LLM layer is fully abstracted** — switching providers requires no core changes.

---

## ▶️ Run Locally

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## 💬 Example Queries

**Analytics**
- "Which category has the highest revenue?"
- "Show revenue by category"
- "Average order value by category"

**Knowledge**
- "What is cama mesa banho?"
- "Define customer lifetime value"

**Follow-ups**
- "Top 5"
- "Only electronics"

**Blocked (Safety)**
- "Predict revenue next year"
- "Drop table orders"

---

## 🧪 Testing
- Intent detection & routing
- Knowledge lookup
- Follow-up handling
- SQL safety & correctness
- Edge cases

All tests pass before submission.

---

## 📦 Repository Structure

```
olist-genai-agent/
├── agent/          # Core agent logic
├── knowledge/      # Glossary & enrichment
├── db/             # DuckDB database
├── tests/          # Automated tests
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

## 🎥 Demo
A **5–7 min demo video** covers:
- Product walkthrough
- Conversational analytics & follow-ups
- Architecture & design decisions

---

## 🔮 Future Enhancements
- Time-series & forecasting
- Deeper seller/product enrichment
- Multi-step analytical reasoning
- Role-based dashboards
- Dockerized cloud deployment

---

## 🏁 Summary
This project demonstrates:
- Practical GenAI agent design
- Safe, deterministic analytics
- Conversational UX with memory
- Clean architecture and extensibility

Built to be **business-ready, explainable, and safe**.

