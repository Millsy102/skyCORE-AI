
import os
import requests
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

HEADERS = {
    "Content-Type": "application/json"
}

def call_gemini(prompt, project_path):
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set")

    HEADERS["Authorization"] = f"Bearer {GEMINI_API_KEY}"

    context_data = gather_context(project_path)

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": context_data + "\n\nTASK: " + prompt}]}
        ]
    }

    response = requests.post(
        GEMINI_API_URL + f"?key={GEMINI_API_KEY}",
        headers=HEADERS,
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

def gather_context(project_path):
    summary_file = os.path.join(project_path, "project_summary.txt")
    context_file = os.path.join(project_path, ".skycontext")
    memory_dir = os.path.join(project_path, ".memory")

    context_pieces = []

    if os.path.exists(summary_file):
        with open(summary_file, "r") as f:
            context_pieces.append(f.read())

    if os.path.exists(context_file):
        with open(context_file, "r") as f:
            context_pieces.append(f.read())

    if os.path.isdir(memory_dir):
        summaries = sorted([
            os.path.join(memory_dir, f) for f in os.listdir(memory_dir)
            if f.startswith("summary_") and f.endswith(".json")
        ])
        for path in summaries[-3:]:
            with open(path, "r") as f:
                context_pieces.append(f.read())

    return "\n\n".join(context_pieces)
