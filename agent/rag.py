# agent/rag.py

from pathlib import Path

KNOWLEDGE_PATH = Path("knowledge/products.md")

def get_context():
    if KNOWLEDGE_PATH.exists():
        return KNOWLEDGE_PATH.read_text(encoding="utf-8")
    return ""
