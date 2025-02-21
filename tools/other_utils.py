def read_file(path: str):
    result = []
    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.rstrip("\n")
            if line and not line.startswith("# "):
                result.append(line)
    return result
