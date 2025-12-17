def wants_chart(text):
    keywords = ["chart", "plot", "visual", "graph", "show"]
    return any(k in text.lower() for k in keywords)
