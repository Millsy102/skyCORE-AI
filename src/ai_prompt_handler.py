
import os
from src import model_manager
from src.agent_log import AgentLog
from src.rules_parser import load_rules, apply_rules_to_prompt

def handle_ai_prompt(prompt, project_path="."):
    log = AgentLog(project_path)
    rules = load_rules(project_path)
    enriched_prompt = apply_rules_to_prompt(prompt, rules)

    log.log_step("prompt", "Sending prompt to model", {"prompt": enriched_prompt})
    try:
        response = model_manager.route_prompt(enriched_prompt, project_path)
        log.log_step("response", "Model response received", {"response": str(response)[:500]})
        log.save_log("ai")
        return response
    except Exception as e:
        log.log_step("error", "Prompt failed", {"error": str(e)})
        log.save_log("ai")
        return {"error": str(e)}
