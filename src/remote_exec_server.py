
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run_code():
    try:
        exec(request.json["code"], globals())
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def start_server():
    app.run(host="0.0.0.0", port=7777)
