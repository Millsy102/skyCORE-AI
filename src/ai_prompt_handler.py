
import os
from src import model_manager
from src.agent_log import AgentLog
from src.rules_parser import load_rules, apply_rules_to_prompt
from src.plugin_builder import extract_plugin_from_response

def handle_ai_prompt(prompt, project_path="."):
    log = AgentLog(project_path)
    rules = load_rules(project_path)
    enriched_prompt = apply_rules_to_prompt(prompt, rules)

    log.log_step("prompt", "Sending prompt to model", {"prompt": enriched_prompt})
    try:
        response = model_manager.route_prompt(enriched_prompt, project_path)
        log.log_step("response", "Model response received", {"response": str(response)[:500]})

        if isinstance(response, str) and "main.py" in response and "```" in response:
            plugin_result = extract_plugin_from_response(response)
            log.log_step("plugin", "Plugin scaffold created", {"result": plugin_result})
        elif isinstance(response, dict) and "candidates" in response:
            response_text = response["candidates"][0]["content"]["parts"][0]["text"]
            if "main.py" in response_text and "```" in response_text:
                plugin_result = extract_plugin_from_response(response_text)
                log.log_step("plugin", "Plugin scaffold created", {"result": plugin_result})

        log.save_log("ai")
        return response
    except Exception as e:
        log.log_step("error", "Prompt failed", {"error": str(e)})
        log.save_log("ai")
        return {"error": str(e)}
