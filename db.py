import psycopg2
import psycopg2.extras
import pytz
import datetime
import logging

# Enable logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("psycopg2")

class DatabaseClient:
    def __init__(self):
        self.conn = psycopg2.connect("dbname=postgres user=postgres")
        logging.basicConfig(level=logging.DEBUG)

    def get_last_created_at(self, api_source):
        with self.conn.cursor() as cur:
            query = "SELECT MAX(created_at) FROM historical_news"
            if api_source:
                query += " WHERE api_source = %s"
            cur.execute(query, (api_source,))
            result = cur.fetchone()
            return result[0] if result and result[0] else datetime.datetime(2024, 1, 1, tzinfo=pytz.UTC)
    
    def insert_transaction(self, symbol, action, quantity, price):
        with self.conn.cursor() as cur:
            cur.execute('''
                INSERT INTO transactions (symbol, action, quantity, price)
                VALUES (%s, %s, %s, %s);
            ''', (symbol, action, quantity, price))
            self.conn.commit()
    
    def bulk_insert_news(self, news_list):
        logging.debug("Entering bulk_insert_news")
        with self.conn.cursor() as cur:
            query = '''
                INSERT INTO historical_news (author, title, url, source, summary, created_at, symbols, api_source)
                VALUES %s
            '''
            logging.debug(f"Inserting {len(news_list)} news articles.")
            psycopg2.extras.execute_values(cur, query, news_list)
            logging.debug("Insertion complete")
            self.conn.commit()

    def bulk_insert_historical_prices(self, price_list):
        with self.conn.cursor() as cur:
            query = '''
                INSERT INTO historical_prices (symbol, timestamp, open_price, high_price, low_price, close_price, volume)
                VALUES %s
                ON CONFLICT (symbol, timestamp) DO NOTHING;
            '''
            psycopg2.extras.execute_values(cur, query, price_list)
            self.conn.commit()
    
    def get_transactions(self, symbol=None):
        with self.conn.cursor() as cur:
            if symbol:
                cur.execute("SELECT * FROM transactions WHERE symbol = %s ORDER BY timestamp DESC;", (symbol,))
            else:
                cur.execute("SELECT * FROM transactions ORDER BY timestamp DESC;")
            return cur.fetchall()
    
    def get_news(self, symbol=None, sentiment=None):
        with self.conn.cursor() as cur:
            query = "SELECT * FROM news WHERE 1=1"
            params = []
            
            if symbol:
                query += " AND %s = ANY(symbols)"
                params.append(symbol)
            if sentiment:
                query += " AND sentiment = %s"
                params.append(sentiment)
            
            query += " ORDER BY created_at DESC;"
            cur.execute(query, tuple(params))
            return cur.fetchall()
    
    def close(self):
        self.conn.close()