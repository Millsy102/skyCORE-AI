
import requests

def check_update(current_version="1.0.0"):
    try:
        latest = requests.get("https://skycore-updates.com/latest.json").json()
        if latest["version"] != current_version:
            return True
    except:
    print('Update fetch failed')
