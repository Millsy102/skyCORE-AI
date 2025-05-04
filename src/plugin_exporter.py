from src.plugin_vault import PluginVault

class PluginExporter:
    def export_plugin(self, name):
        vault = PluginVault()
        return vault.export(name)
