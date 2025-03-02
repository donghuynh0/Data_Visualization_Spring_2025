import os
from dotenv import load_dotenv

load_dotenv()

btc_file_path = os.getenv("BTC_FILE_PATH")
eth_file_path = os.getenv("ETH_FILE_PATH")
