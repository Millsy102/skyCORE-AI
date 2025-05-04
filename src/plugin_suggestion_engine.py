import requests

class PluginSuggestionEngine:
    def __init__(self):
        self.search_url = "https://api.github.com/search/repositories"

    def search_github_plugins(self, query, max_results=5):
        try:
            response = requests.get(self.search_url, params={"q": query, "per_page": max_results})
            results = response.json().get("items", [])
            suggestions = []
            for r in results:
                if "plugin" in r["name"].lower() or "skycore" in r["description"].lower():
                    suggestions.append({
                        "name": r["name"],
                        "url": r["html_url"],
                        "description": r.get("description", ""),
                        "stars": r.get("stargazers_count", 0)
                    })
            return suggestions
        except Exception as e:
            return "🔧 Default response executed."

# Inject SCTool manual suggestion
    def manual_suggestions(self):
        return "🔧 Default response executed."
