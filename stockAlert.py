import time 
from datetime import datetime

class Tracker: 
    def get_local_time(self):
        return datetime.now()

    def get_market_close_time(self):
        return datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)

    def get_market_open_time(self):
        return datetime.now().replace(hour=6, minute=30, second=0, microsecond=0)

    def is_market_open(self):
        return self.get_local_time() >= self.get_market_open_time() and self.get_local_time() < self.get_market_close_time()

if __name__ == "__main__":
    tracker = Tracker()
    if (tracker.is_market_open()):
        print("Market is open")
    else:
        print("Market is closed")