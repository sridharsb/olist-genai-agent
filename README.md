🛒 Olist GenAI Analytics Assistant

An AI-powered, conversational analytics agent that enables users to explore and analyze the Brazilian Olist e-commerce dataset using natural language.

Built as a GenAI agentic system, the assistant combines:

Rule-based + LLM intent detection

SQL analytics over curated views

Knowledge enrichment beyond raw tables

Conversational memory and follow-ups

A clean, modern Streamlit UI with visual insights

🎯 Problem Statement

E-commerce datasets are rich but difficult to explore without SQL expertise.

This project allows business users to ask questions like:

“Which category has the highest revenue?”

“Show revenue by category” → “Top 3”

“What is cama mesa banho?”

“Average order value by category”

…and receive:

Accurate analytical results

Visualizations

Business-friendly explanations

Context-aware follow-ups

🚀 Key Features
🧠 Agentic Intelligence

Hybrid rule-based + LLM intent detection

Conversational memory (supports follow-ups like “top 5”)

Safe SQL generation with strict guardrails

Metric and category disambiguation

📊 Analytics Engine

DuckDB analytics over pre-aggregated SQL views

Revenue, units sold, AOV, CLV, customer and seller insights

Fast, deterministic query execution

Robust filtering (category, year, limits)

📚 Knowledge Enrichment

Category explanations (Portuguese ↔ English aliases)

Metric definitions (AOV, CLV, revenue, etc.)

Product context beyond the dataset

Business insight generation (“Why this category performs well”)

🎨 Modern UI (Streamlit)

Conversational chat interface

KPI metric cards

Clean tables and readable charts

Explain-on-demand insights

Graceful handling of unsupported queries

🧩 System Architecture (High Level)
User
 ↓
Streamlit UI
 ↓
Conversation Router
 ├─ Knowledge Lookup (definitions, categories)
 ├─ Intent Detection (rules + LLM fallback)
 ├─ Follow-up Resolution (memory)
 ↓
SQL Builder (views only)
 ↓
DuckDB Analytics
 ↓
Results + Insights

🛠 Tech Stack
Layer	Technology
UI	Streamlit
Database	DuckDB
Data	Olist Brazilian E-commerce Dataset
LLM	Local LLM (LM Studio / Ollama) or Gemini
Analytics	SQL Views
Charts	Matplotlib
Testing	Custom test harness
🤖 LLM Setup (Important)

This project supports multiple LLM deployment modes.

✅ Option 1: Local LLM (Default)

Tested with LM Studio / Ollama

Example models: Qwen2.5, LLaMA, Mistral

No API keys required

Ideal for offline demos and reproducibility

☁️ Option 2: Cloud LLM

Google Gemini (via Google AI Studio)

OpenRouter (free-tier models)

OpenAI-compatible APIs

🔧 The LLM layer is fully abstracted — switching providers requires no changes to core agent logic.

▶️ How to Run Locally
# Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py

💬 Example Questions to Ask
Conversational

“Hi”

“What can you do?”

“Tell me about the dataset”

Knowledge

“What is cama mesa banho?”

“What are bed bath products?”

“Define customer lifetime value”

Analytics

“Which category has the highest revenue?”

“Show revenue by category”

“Average order value by category”

Follow-ups

“Top 5”

“Top 3”

“Show revenue for bed bath”

Safety

“predict revenue next year”

“drop table orders”

🧪 Testing

The agent includes a comprehensive automated test suite covering:

Conversation handling

Knowledge lookup

Intent detection

Follow-ups

SQL safety

Metric correctness

Edge cases

All tests pass successfully before submission.

📦 Repository Structure
olist-genai-agent/
│
├── agent/               # Core agent logic
├── knowledge/            # Glossary & enrichment data
├── db/                   # DuckDB database
├── tests/                # Automated tests
├── streamlit_app.py      # UI entry point
├── requirements.txt
└── README.md

🎥 Demo Video

A 5–7 minute demo video accompanies this submission, covering:

Product walkthrough

Conversational analytics

Follow-ups and insights

Architecture and design decisions

🔮 Future Enhancements

If more time were available:

Time-series forecasting

Seller & product name enrichment

Multi-turn analytical reasoning

Role-based dashboards

Cloud deployment (Docker + API)

🏁 Conclusion

This project demonstrates:

Strong problem solving

Practical GenAI system design

Agentic reasoning with memory

Clean UX and thoughtful engineering tradeoffs

It is designed to be extensible, safe, and business-ready.


High-level architecture

┌────────────────────────────┐
│           User             │
│  Natural Language Query    │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│       Streamlit UI         │
│  • Chat Input              │
│  • KPI Cards               │
│  • Tables & Charts         │
│  • Explain Button          │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│   Conversation Router      │
│  • Greetings               │
│  • Small Talk              │
│  • Help / Dataset Info     │
│  • Safety Checks           │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│     GenAI Agent Core       │
│                            │
│  ┌──────────────────────┐ │
│  │ Intent Detection     │ │
│  │ • Rule-based         │ │
│  │ • LLM fallback       │ │
│  └──────────────────────┘ │
│                            │
│  ┌──────────────────────┐ │
│  │ Memory & Follow-ups  │ │
│  │ • Last intent        │ │
│  │ • Filters (top N)    │ │
│  └──────────────────────┘ │
│                            │
│  ┌──────────────────────┐ │
│  │ Knowledge Layer      │ │
│  │ • Definitions        │ │
│  │ • Category aliases   │ │
│  │ • Product context    │ │
│  └──────────────────────┘ │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│     SQL Builder Layer      │
│  • View-only queries       │
│  • Filters & limits        │
│  • SQL guardrails          │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│        DuckDB              │
│  • Analytics Views         │
│  • Revenue, AOV, CLV       │
│  • Category aggregates     │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│  Insights & Explanation    │
│  • Business reasoning      │
│  • Category performance    │
│  • LLM-generated insights  │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│   UI Rendering Layer       │
│  • Charts                 │
│  • Tables                 │
│  • Explanations            │
└────────────────────────────┘

2️⃣ Detailed Agent Flow (Technical Deep Dive)

“what happens when a user asks a question”

User Query
   │
   ▼
[Streamlit Input]
   │
   ▼
[Conversation Handler]
   ├── Greeting? → Static response
   ├── Definition? → Knowledge lookup
   ├── Unsafe SQL? → Block
   └── Otherwise → Agent Core
   │
   ▼
[Intent Resolver]
   ├── Rule-based intent match
   ├── If not found → LLM intent classifier
   └── If follow-up → Use memory
   │
   ▼
[Metric & Context Resolution]
   ├── Revenue vs AOV vs Units
   ├── Category alias translation (EN ↔ PT)
   ├── Explicit override handling
   └── Apply follow-up constraints (top N)
   │
   ▼
[SQL Construction]
   ├── Select from pre-built views
   ├── Apply WHERE filters
   ├── Preserve ORDER BY
   ├── Apply LIMIT safely
   └── Validate SQL
   │
   ▼
[DuckDB Execution]
   │
   ▼
[Result DataFrame]
   │
   ▼
[Insight Generator]
   ├── Identify top category
   ├── Attach business reasons
   └── Generate explanation text
   │
   ▼
[Streamlit Rendering]
   ├── KPI cards
   ├── Chart / Table toggle
   ├── Explain button
   └── Download CSV

3️⃣ Mermaid Diagram

flowchart TD

U[User] --> UI[Streamlit UI]

UI --> CR[Conversation Router]

CR -->|Greeting / Help| R1[Static Response]
CR -->|Definition| K[Knowledge Layer]
CR -->|Analytics| AC[Agent Core]

AC --> IR[Intent Resolver]
IR -->|Rules| I1[Matched Intent]
IR -->|Fallback| LLM[LLM Intent Classifier]

AC --> MEM[Conversation Memory]
AC --> KL[Knowledge & Category Aliases]

AC --> SQLB[SQL Builder]
SQLB --> SG[SQL Guardrails]
SG --> DB[DuckDB Views]

DB --> DF[Result DataFrame]

DF --> INS[Insight Generator]
INS --> UI

UI --> CH[Charts & Tables]
UI --> EXP[Explain Button]

👋 Thank you for reviewing!
