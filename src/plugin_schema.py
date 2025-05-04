# 📦 Module imports
import os
import yaml
from jsonschema import validate, ValidationError
from src.logging_engine import log_trace

# Class: PluginSchemaValidator: — defines main behavior for plugin_schema.py
class PluginSchemaValidator:
# Function: __init__ — handles a core step in this module
    def __init__(self, schema_path="config/plugin_schema.yaml"):
        self.schema_path = schema_path
        self.schema = self._load_schema()

# Function: _load_schema — handles a core step in this module
    def _load_schema(self):
        if not os.path.exists(self.schema_path):
            raise FileNotFoundError(f"Missing schema file: {self.schema_path}")
        with open(self.schema_path, "r", encoding="utf-8") as f:
            schema = yaml.safe_load(f)
        log_trace("PluginSchemaValidator", "_load_schema", "init", "Schema loaded")
    # 🏁 Returning result
        return schema

# Function: validate_plugin_metadata — handles a core step in this module
    def validate_plugin_metadata(self, plugin_yaml_path: str) -> bool:
        if not os.path.exists(plugin_yaml_path):
            log_trace("PluginSchemaValidator", "validate_plugin_metadata", "error", f"Missing file: {plugin_yaml_path}")
    # 🏁 Returning result
            return False
        with open(plugin_yaml_path, "r", encoding="utf-8") as f:
            plugin_data = yaml.safe_load(f)
        try:
            validate(instance=plugin_data, schema=self.schema)
            log_trace("PluginSchemaValidator", "validate_plugin_metadata", "success", f"Validated {plugin_yaml_path}")
    # 🏁 Returning result
            return True
        except ValidationError as e:
            log_trace("PluginSchemaValidator", "validate_plugin_metadata", "fail", f"{plugin_yaml_path} failed validation: {str(e)}")
    # 🏁 Returning result
            return False
