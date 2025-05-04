
class ModelStats:
    def __init__(self):
        self.token_count = 0
        self.model = 'gpt-4'

    def update(self, tokens):
        self.token_count += tokens

    def reset(self):
        self.token_count = 0

    def get_summary(self):
        return {
            'model': self.model,
            'tokens_used': self.token_count,
            'estimated_cost': round(self.token_count * 0.00002, 4)  # simulated price/token
        }
