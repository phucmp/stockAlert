import os
import websocket
import requests
from dotenv import load_dotenv
from datetime import datetime

class Trades:
    def __init__(self, ticker, token):
        self.url = "wss://ws.finnhub.io?token=" + token
        self.ticker = ticker

    def _on_message(self, ws, message):
        print(message)

    def _on_error(self, ws, error):
        print(error)

    def _on_close(self, ws):
        print("### Closed ###")

    def _on_open(self, ws):
        ws.send('{"type":"subscribe","symbol":"' + self.ticker + '"}')

    def start(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(self.url, on_message=self._on_message, on_error=self._on_error, on_close=self._on_close)
        ws.on_open = self._on_open
        ws.run_forever()

class Program: 
    def __init__(self):
        load_dotenv()
        self.api_token = os.environ.get("FINNHUB_API_KEY")
        self.api_uri = 'https://finnhub.io/api/v1/quote?symbol='

    def get_local_time(self):
        return datetime.now()

    def get_market_close_time(self):
        return datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)

    def get_market_open_time(self):
        return datetime.now().replace(hour=6, minute=30, second=0, microsecond=0)

    def is_market_open(self):
        return self.get_local_time() >= self.get_market_open_time() and self.get_local_time() < self.get_market_close_time()

    def get_quote(self):
        url = self.api_uri + self.ticker + '&token=' + self.api_token
        r = requests.get(url)
        print(r.json())

    def start(self):
        self.ticker = input("Enter Your Stock Ticker: ").upper()
        if (self.is_market_open()):
            trades = Trades(self.ticker, self.api_token)
            trades.start()
        else:
            self.get_quote()

if __name__ == "__main__":
    program = Program()
    program.start()