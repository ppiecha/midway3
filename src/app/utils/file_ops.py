def write_file(full_path: str, content: str):
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)


def read_file(full_path: str) -> str:
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()
