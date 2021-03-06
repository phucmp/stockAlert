import os
import sys
import websocket
import requests
import json
from dotenv import load_dotenv
from datetime import datetime

class Trades:
    def __init__(self, ticker, token):
        self.url = "wss://ws.finnhub.io?token=" + token
        self.ticker = ticker
        self.prev_price = -1

    def _on_message(self, ws, message):
        try:
            data = json.loads(message)['data'][0]
            price = data['p']
            if self.prev_price == -1:
                print("\n------------------")
                print("$" + self.ticker + '\n')
                print("Current Price: $" + str(price))
            else:
                if price > self.prev_price * 1.20:
                    print("Up by more than 20%: $" + str(price))
                    print("!!!! MOON TIME !!!!")
                elif price > self.prev_price * 1.1:
                    print("Up by 10%: $" + str(price))
                elif price > self.prev_price * 1.05:
                    print("Up by 5%: $" + str(price))
                elif price < self.prev_price * 0.95:
                    print("Down by 5%: $" + str(price))
                elif price < self.prev_price * 0.9:
                    print("Down by 10%: $" + str(price))
                elif price < self.prev_price * 0.8:
                    print("Down by more than 20%: $" + str(price))
                    print("!!!! SALE: BUY MORE !!!!")
            self.prev_price = price
        except:
            pass

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
    
    def get_analysis(self, close, prev_close):
        if close > prev_close:
            return 'BULLISH'
        elif close < prev_close:
            return 'BEARISH'
        else:
            return 'STEADY'

    def get_quote(self):
        url = self.api_uri + self.ticker + '&token=' + self.api_token
        response = requests.get(url).json()
        print("------------------")
        print("$" + self.ticker + ":\n")
        print("$" + str(response['h']), ": High Price")
        print("$" + str(response['l']), ": Low Price")
        print("$" + str(response['o']), ": Open Price")
        print("$" + str(response['c']), ": Close Price")
        print("$" + str(response['pc']), ": Previous Close Price\n")
        print("Analysis: ", self.get_analysis(response['c'], response['pc']))
        print("------------------")

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