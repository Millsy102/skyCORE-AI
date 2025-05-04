
class AffinityEngine:
    def __init__(self):
        self.profile = {
            "favorite_persona": "Nova",
            "theme": "Matrix",
            "voice": "Luna",
        }

    def recommend(self):
        return f"🎯 Using your preferences: {self.profile}"
