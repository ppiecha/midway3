

def write_file(full_path: str, content: str):
    with open(full_path, 'w') as f:
        f.write(content)

def read_file(full_path: str) -> str:
    with open(full_path, 'r') as f:
        return f.read()