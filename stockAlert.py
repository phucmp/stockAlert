import time 
from datetime import datetime

class Program: 
    def get_local_time(self):
        return datetime.now()

    def get_market_close_time(self):
        return datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)

    def get_market_open_time(self):
        return datetime.now().replace(hour=6, minute=30, second=0, microsecond=0)

    def is_market_open(self):
        return self.get_local_time() >= self.get_market_open_time() and self.get_local_time() < self.get_market_close_time()

    def start(self):
        self.ticker = raw_input("Enter Your Stock Ticker: ")
        while(self.is_market_open()):
            print("Market is open")
            print("Tracking: $" + self.ticker)
            time.sleep(20)

if __name__ == "__main__":
    program = Program()
    program.start()