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

    def get_news_sentiment(self, news_content):
        try:
            sentiment_response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Analyze the sentiment of this news text as Positive, Neutral, or Negative."},
                    {"role": "user", "content": news_content}
                ]
            )

            return sentiment_response.choices[0].message.content
        except Exception as e:
            print(f"Error fetching sentiment for {ticker}: {e}")
            return "Neutral"