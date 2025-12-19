# Quick Start Guide

## Setup Complete! ✅

Your Olist GenAI Agent is ready to use. Here's how to get started:

## 1. Verify Setup (Optional)

```bash
python setup_check.py
```

Expected output:
```
[OK] All dependencies installed
[OK] Data files found
[OK] Database setup complete (16 views found)
[OK] Setup complete!
```

## 2. Start the Agent

### Windows:
```bash
run_agent.bat
```

### Or manually:
```bash
venv\Scripts\activate
streamlit run streamlit_app.py
```

## 3. Use the Agent

1. Open your browser to `http://localhost:8501`
2. Type a question in the input box, for example:
   - "Which category has the highest revenue?"
   - "Show revenue by category"
   - "What is the average order value?"
   - "Top 10 products by revenue"

## Important Notes

### LLM Service (Optional)
- The agent works **without** an LLM service using rule-based intent detection
- For AI explanations, you can optionally run LM Studio locally on port 8000
- If LLM is not available, the agent will skip AI explanations but still work for queries

### Database
- Database is already set up at `db/olist.db`
- Contains 16 analytics views ready for queries
- If you need to rebuild: `python db/setup_db.py`

## Troubleshooting

**Port already in use?**
```bash
streamlit run streamlit_app.py --server.port 8502
```

**Database errors?**
```bash
python db/setup_db.py
```

**Missing packages?**
```bash
pip install -r requirements.txt
```

## Next Steps

- Try different query types (see README.md for full list)
- Explore the analytics views in the database
- Customize the agent by modifying `agent/agent_core.py`
- Add new intents in `agent/intent_map.py` and `agent/sql_templates.py`

