import asyncio
import pandas as pd
import pytz
import os
import subprocess
from binance import AsyncClient, BinanceSocketManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# Define Vietnam Timezone (UTC+7)
vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")

# File paths
btc_file_path = os.getenv("BTC_FILE_PATH")
eth_file_path = os.getenv("ETH_FILE_PATH")

# Ensure CSV files exist
for file in [btc_file_path, eth_file_path]:
    if not os.path.exists(file):
        pd.DataFrame(columns=["Time", "Open", "High", "Low", "Close", "Volume"]).to_csv(file, index=False)

# Counter to track fetches
fetch_counter = 0
FETCH_LIMIT = 6  # Push to GitHub after every 6 fetches

async def fetch_binance_data(symbol, file_path):
    """Fetch real-time price data for a given symbol and save to CSV."""
    global fetch_counter
    client = await AsyncClient.create(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY)
    bm = BinanceSocketManager(client)
    socket = bm.kline_socket(symbol, interval="1m")

    async with socket as stream:
        print(f"Listening for {symbol} price updates...")
        while True:
            msg = await stream.recv()
            if msg['e'] == 'kline' and msg['k']['x']:  # Only closed candles
                kline = msg['k']
                time_vietnam = pd.to_datetime(kline['t'], unit='ms').tz_localize('UTC').tz_convert(vietnam_tz)
                
                data = {
                    "Time": time_vietnam.strftime('%Y-%m-%d %H:%M:%S'),
                    "Open": float(kline['o']),
                    "High": float(kline['h']),
                    "Low": float(kline['l']),
                    "Close": float(kline['c']),
                    "Volume": float(kline['v'])
                }
                
                df = pd.DataFrame([data])
                df.to_csv(file_path, mode='a', header=False, index=False)

                fetch_counter += 1
                print(f"Saved {symbol} price data ({fetch_counter}/{FETCH_LIMIT})")

                # Auto-push to GitHub every 5 fetches
                if fetch_counter >= FETCH_LIMIT:
                    await push_to_github()
                    fetch_counter = 0  # Reset counter

    await client.close_connection()

async def push_to_github():
    """Push updated data to GitHub."""
    print("Pushing data to GitHub...")

    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update crypto data"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Successfully pushed to GitHub!")
    except subprocess.CalledProcessError as e:
        print(f"❌ GitHub push failed: {e}")

async def main():
    """Run BTC and ETH WebSocket fetchers concurrently."""
    await asyncio.gather(
        fetch_binance_data("BTCUSDT", btc_file_path),
        fetch_binance_data("ETHUSDT", eth_file_path)
    )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
