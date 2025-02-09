import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class GPTValidator:
    def __init__(self):
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)

    def validate_trade_with_gpt(self, stock1, stock2, z_score):
        prompt = f"""
            I am a trading bot analyzing a statistical arbitrage setup.
            Stock 1: {stock1}, Stock 2: {stock2}
            Z-score: {z_score}

            Should I enter this trade based on historical behavior?
            Respond with 'YES' or 'NO' and a brief reason.
        """
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        decision = response.choices[0].message.content
        return "YES" in decision