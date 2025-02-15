import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class GPTValidator:
    def __init__(self):
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)

    def get_news_sentiment(self, news_content):
        if not news_content:
            return "Neutral", 0.0
        
        try:
            system_prompt = """Pretend you are an expert financial quant trader who is holding the AAPL stock. You will be analyzing the following news articles to determine the sentiment score of the news articles and the stock price of AAPL. +1 for positive sentiment, -1 for negative sentiment, 0 for neutral sentiment. The sentiment score will be used to determine if you should hold, buy, or sell the stock, and it should only range from -1 to 1, with -1 being bearish and +1 being bullish. Reply using the following template
    
            [Example Reply]:
            +1, Bullish
            -1, Bearish
            0, Neutral

            Here are the news articles to analyze:

            """
            sentiment_response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages= [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": news_content}
                ]
            )
            result = sentiment_response.choices[0].message.content.split(";")
            return result[0], float(result[1])
        except:
            return "Neutral", 0.0