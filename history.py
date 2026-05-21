import json
from datetime import datetime

def save_history(values, result):

    data = {
        "time": str(datetime.now()),
        "values": values[0].tolist(),
        "result": str(result)   # FIX IMPORTANT
    }

    try:
        with open("history.json", "r") as f:
            old = json.load(f)
    except:
        old = []

    old.append(data)

    with open("history.json", "w") as f:
        json.dump(old, f, indent=4)