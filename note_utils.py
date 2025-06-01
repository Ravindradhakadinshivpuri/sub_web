def save_note(content, filename="notes.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def load_note(filename="notes.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def log_user_access(ip, user_agent):
    import json
    import os
    log_file = "visitors.json"
    data = []
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    entry = {"ip": ip, "user_agent": user_agent}
    data.append(entry)
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
