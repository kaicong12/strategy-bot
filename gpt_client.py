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
        if not news_content:
            return "Neutral", 0.0
        try:
            sentiment_response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Analyze the sentiment of this news text as Positive, Neutral, or Negative, and return a sentiment score between -1 (Negative) to 1 (Positive)."},
                    {"role": "user", "content": news_content}
                ]
            )
            result = sentiment_response.choices[0].message.content.split(";")
            return result[0], float(result[1])
        except:
            return "Neutral", 0.0