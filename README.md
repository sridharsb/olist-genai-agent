# Olist GenAI Agent

A conversational analytics assistant for the Brazilian Olist e-commerce dataset (2016-2018). This agent allows you to query sales data using natural language and get insights through an interactive Streamlit interface.

## Features

- **Natural Language Queries**: Ask questions in plain English about revenue, sales, products, customers, and more
- **Interactive Dashboard**: Streamlit-based UI with charts, tables, and insights
- **Multiple Analytics**: Revenue analysis, product performance, customer lifetime value, seller analytics, and more
- **AI Explanations**: Optional LLM-powered explanations for query results
- **Knowledge Base**: Built-in glossary and product category enrichment

## Prerequisites

- Python 3.8+
- Virtual environment (recommended)
- Olist dataset CSV files in the `data/` directory

## Setup

### 1. Install Dependencies

```bash
# Activate virtual environment (if using one)
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

# Install required packages
pip install -r requirements.txt
```

### 2. Set Up Database

The database should already be set up, but if you need to recreate it:

```bash
python db/setup_db.py
```

This will:
- Load all CSV files from the `data/` directory
- Create DuckDB database with analytics views
- Set up optimized views for common queries

### 3. Verify Setup

Run the setup verification script:

```bash
python setup_check.py
```

This checks:
- ✅ All dependencies are installed
- ✅ Data files are present
- ✅ Database and views are set up correctly

### 4. (Optional) Configure LLM Service

The agent works with rule-based intent detection by default. For AI-powered explanations and fallback intent detection, you can optionally set up:

**Option A: LM Studio (Local)**
1. Install and run [LM Studio](https://lmstudio.ai/)
2. Load a model (e.g., `qwen2.5-7b-instruct`)
3. Start the local server on port 8000
4. The agent is already configured to use `http://localhost:8000/v1`

**Option B: OpenAI API**
Modify `agent/llm_client.py` to use OpenAI's API:
```python
client = OpenAI(api_key="your-api-key")
```

**Note**: The agent works fine without LLM - it will use rule-based intent detection and skip AI explanations.

## Running the Agent

### Option 1: Using the Batch Script (Windows)

```bash
run_agent.bat
```

### Option 2: Manual Start

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

# Run Streamlit app
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## Example Queries

- "Which category has the highest revenue?"
- "Show revenue by category"
- "What is the average order value?"
- "Top 10 products by revenue"
- "Monthly revenue trend"
- "Customer lifetime value by state"
- "Payment type analysis"

## Project Structure

```
olist-genai-agent/
├── agent/                 # Core agent modules
│   ├── agent_core.py      # Main agent logic
│   ├── intent_resolver.py # Rule-based intent detection
│   ├── llm_intent.py      # LLM-based intent detection
│   ├── sql_templates.py   # SQL query templates
│   ├── conversation.py    # Conversation handling
│   ├── knowledge.py       # Knowledge base integration
│   └── ...
├── data/                  # Olist dataset CSV files
├── db/                    # DuckDB database
│   ├── olist.db          # Main database file
│   └── setup_db.py       # Database setup script
├── knowledge/             # Knowledge base files
│   ├── glossary.json     # Business term definitions
│   └── product_enrichment.json
├── streamlit_app.py      # Streamlit UI
├── setup_check.py        # Setup verification
└── requirements.txt      # Python dependencies
```

## Supported Analytics

### Revenue Analytics
- Highest/lowest revenue category
- Revenue by category
- Yearly/monthly revenue trends
- Category revenue by year

### Sales Analytics
- Most/least selling categories
- Units sold by category

### Product Analytics
- Top products by revenue/units
- Product performance metrics

### Customer Analytics
- Customer lifetime value
- Top customers by state

### Seller Analytics
- Top sellers by revenue
- Seller performance by state

### Payment Analytics
- Payment type analysis

### Order Value Analytics
- Average order value (AOV)
- AOV by category

## Troubleshooting

### Database Issues
If you see database errors:
```bash
python db/setup_db.py
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### LLM Connection Errors
The agent works without LLM. If you see connection errors, the agent will fall back to rule-based intent detection. To use LLM features:
- Ensure LM Studio is running (for local setup)
- Or configure OpenAI API key in `agent/llm_client.py`

### Port Already in Use
If port 8501 is in use:
```bash
streamlit run streamlit_app.py --server.port 8502
```

## License

This project is for educational and demonstration purposes.

