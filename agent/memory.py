# agent/memory.py

_state = {
    "last_intent": None,
    "last_modifiers": {},
    "last_entities": {}
}

def remember_intent(intent: str):
    _state["last_intent"] = intent

def remember_modifiers(modifiers: dict):
    _state["last_modifiers"] = modifiers or {}

def remember_entities(entities: dict):
    _state["last_entities"].update(entities or {})

def last_intent():
    return _state["last_intent"]

def get_modifiers():
    return _state["last_modifiers"]

def get_entities():
    return _state["last_entities"]

def reset_memory():
    _state["last_intent"] = None
    _state["last_modifiers"] = {}
    _state["last_entities"] = {}
