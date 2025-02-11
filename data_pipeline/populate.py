# 1. Use alpha_vantage to fetch news relevant to ticker
# 2. Use alpaca to fetch historical prices for ticker
# 3. Configure cronjob to run this script everyday at pre-market timings

import os
import sys
# Add the parent directory to Python's path so we can access config.py
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import requests
import datetime
from db import DatabaseClient
from dotenv import load_dotenv
load_dotenv()

# modify TICKER to get news for a different stock, via the alpaca and alpha_vantage api
TICKER = "AAPL"
def fetch_alpaca_news(db_client):
    last_created_at = db_client.get_last_created_at("alpaca")
    url = "https://data.alpaca.markets/v1beta1/news"
    params = {
        "limit": 50, 
        "start": (last_created_at + datetime.timedelta(seconds=1)).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "sort": "asc",
        "symbols": TICKER
    }
    next_token = None
    news_list = []

    while True:
        print(params)
        if next_token:
            params["page_token"] = next_token

        response = requests.get(url, headers={
            "accept": "application/json",
            "APCA-API-KEY-ID": os.getenv("ALPACA_API_KEY"),
            "APCA-API-SECRET-KEY": os.getenv("ALPACA_SECRET_KEY"),
        }, params=params).json()

        print(f"Found {len(response.get('news', []))} news articles.")
        fetched_news = response.get("news", [])
        for news in fetched_news:
            # sentiment_label, sentiment_score = gpt_validator.get_news_sentiment(news.get("content", "") or news.get("summary", ""))
            news_list.append((
                news.get("author"),
                news.get("headline") or news.get("title"),
                news.get("url"),
                news.get("source"),
                news.get("summary"),
                news.get("created_at"),
                news.get("symbols"),
                "alpaca"
                # sentiment_label,
                # sentiment_score
            ))
        
        if news_list:
            db_client.bulk_insert_news(news_list)
            news_list.clear()
        
        next_token = response.get("next_page_token")
        if not fetched_news:
            break
        
        if not next_token:
            latest_news_time = max(news["created_at"] for news in fetched_news)
            if latest_news_time > last_created_at.strftime('%Y-%m-%dT%H:%M:%SZ'):
                # add 1 milisecond to the next query
                params["start"] = (datetime.datetime.strptime(latest_news_time, '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(seconds=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
                next_token = None
            else:
                break

        print(f"Retrying using the next page token: {next_token}")

def fetch_alpha_vantage_news(db_client):
    last_created_at = db_client.get_last_created_at("alpha_vantage")
    url = "https://www.alphavantage.co/query"
    last_fetched_time = (last_created_at + datetime.timedelta(seconds=1)).strftime("%Y%m%dT%H%M")
    news_list = []
    
    while True:
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": "AAPL",
            "time_from": last_fetched_time,
            "apikey": os.getenv("ALPHA_VANTAGE_API_KEY"),
            "sort": "EARLIEST",
            "limit": 1000
        }
        response = requests.get(url, params=params).json()
        feed = response.get("feed", [])
        
        print(f"Found {len(feed)} news articles, using params: {params}")
        if not feed:
            break
        
        for news in feed:
            news_list.append((
                news.get("author"),
                news.get("title"),
                news.get("url"),
                news.get("source"),
                news.get("summary"),
                news.get("time_published"),
                [ticker.get("ticker") for ticker in news.get("ticker_sentiment", [])],
                "alpha_vantage",
            ))
        
        if news_list:
            db_client.bulk_insert_news(news_list)
            news_list.clear()
        
        last_fetched_time = feed[-1]["time_published"]

if __name__ == "__main__":
    db_client = DatabaseClient()
    try:
        fetch_alpaca_news(db_client)
        # fetch_alpha_vantage_news(db_client)
        print("Data population completed.")
    finally:
        db_client.close()