import re

def validate_sql(sql: str):
    cleaned = sql.strip().lower()

    if not cleaned.startswith("select"):
        raise ValueError("Only SELECT queries allowed")

    if ";" in cleaned:
        raise ValueError("Multiple SQL statements not allowed")

    forbidden = r"\b(drop|delete|update|insert|alter|truncate)\b"
    if re.search(forbidden, cleaned):
        raise ValueError("Unsafe SQL detected")

    return True
