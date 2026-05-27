import json
from datetime import datetime

LOG_FILE = "logs/access_logs.json"


def log_event(username, role, device, network, decision):

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "username": username,
        "role": role,
        "device": device,
        "network": network,
        "decision": decision,
    }

    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
    except:
        logs = []

    logs.append(log_entry)

    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)

    print(f"Event logged: {log_entry}")  # Print the logged event

    return log_entry


def create_log_file():
    try:
        with open(LOG_FILE, "x") as file:
            json.dump([], file)
            print(f"Log file created: {LOG_FILE}")
    except FileExistsError:
        print(f"Log file already exists: {LOG_FILE}")

    return
