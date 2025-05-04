
import os
import importlib

TAB_GROUPS = {
    "🧠 AI Core": ["chat_tab", "companions_tab", "persona_tab", "mood_tab"],
    "🛠 Development": ["skydevtab", "builder_tab", "evaluator_tab", "plugin_tab", "project_tab", "docs_tab"],
    "🎛 System Control": ["settings_tab", "updater_tab", "theme_tab", "snapshots_tab", "vault_tab"],
    "🎨 UI & Voice": ["gallery_tab", "voice_tab", "rp_mode_tab", "about_tab"],
    "📚 Models & Training": ["memory_tab", "modeltools_tab", "model_tab", "training_tab"],
    "📁 Project Tools": ["terminal_tab", "fixes_tab", "library_tab"],
    "❓ Misc": []
}

def load_group_tabs(runtime, group_name):
    from ui.tabs import __path__ as tab_path
    loaded_tabs = {}
    files = TAB_GROUPS.get(group_name, [])
    for file in files:
        module_name = f"ui.tabs.{file}"
        try:
            module = importlib.import_module(module_name)
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type) and "Tab" in attr:
                    loaded_tabs[attr] = obj(runtime)
        except Exception as e:
    return loaded_tabs

def list_tab_groups():
    return list(TAB_GROUPS.keys())
