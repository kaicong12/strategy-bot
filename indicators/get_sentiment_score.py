import os
import sys
# Add the parent directory to Python's path so we can access config.py
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import datetime
from db import DatabaseClient
from gpt_client import GPTValidator
from dotenv import load_dotenv
load_dotenv()

db = DatabaseClient()
openai_client = GPTValidator()
def get_pass_weeks_news(current_date):
    one_week_ago = current_date - datetime.timedelta(days=7)
    query = '''
        SELECT * FROM historical_news
        WHERE created_at >= %s AND created_at <= %s
        ORDER BY created_at DESC
        LIMIT 10
    '''
    with db.conn.cursor() as cur:
        cur.execute(query, (one_week_ago, current_date))
        past_news = cur.fetchall()
        return past_news

def get_sentiment_score(news):
    return openai_client.get_news_sentiment(news)

def get_stock_data(symbol, current_date):
    
    pass

if __name__ == "__main__":
    current_date = datetime.datetime.now()
    past_week_news = get_pass_weeks_news(current_date)
    
    news_to_analyze = ""
    for news in past_week_news:
        news_summary = news[5].strip()
        if not news_summary:
            continue

        news_to_analyze += f"""
    News Date: {news[6]}
    News Title: {news[2]}
    News Summary: {news[5]}

    """
    
    # sentiment_score = get_sentiment_score(news_to_analyze)
    # print(sentiment_score, 'this is score')




