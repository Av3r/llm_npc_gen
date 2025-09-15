
def load_story(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()