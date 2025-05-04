from flask import Flask, request, jsonify
from src.plugin_executor import PluginExecutor

app = Flask(__name__)
executor = PluginExecutor()

@app.route("/run", methods=["POST"])
def run_plugin():
    data = request.json
    result = executor.run(data["name"], data.get("input", {}))
    return jsonify(result)

def start_server():
    app.run(port=8787)
