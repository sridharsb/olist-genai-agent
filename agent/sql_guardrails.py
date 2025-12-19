"""
SQL validation and security guardrails.
"""

import re


def validate_sql(sql: str) -> bool:
    """
    Validate SQL query for safety and correctness.
    
    Args:
        sql: SQL query string to validate
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If SQL is unsafe or invalid
    """
    if not sql or not isinstance(sql, str):
        raise ValueError("SQL query must be a non-empty string")
    
    cleaned = sql.strip().lower()

    if not cleaned.startswith("select"):
        raise ValueError("Only SELECT queries allowed")

    if ";" in cleaned:
        raise ValueError("Multiple SQL statements not allowed")

    forbidden = r"\b(drop|delete|update|insert|alter|truncate|create|exec|execute)\b"
    if re.search(forbidden, cleaned):
        raise ValueError("Unsafe SQL detected")

    return True
