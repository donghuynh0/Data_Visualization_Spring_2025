import os
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

btc_file_path = os.getenv("BTC_FILE_PATH")
eth_file_path = os.getenv("ETH_FILE_PATH")
