import pandas as pd
import pytz
from binance import AsyncClient, BinanceSocketManager
from logging_config import get_logger
from config import BINANCE_API_KEY, BINANCE_SECRET_KEY

logger = get_logger(__name__)

vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")

async def fetch_binance_data(symbol, file_path, stop_event):
    """Fetch Binance data and save it to a CSV file."""
    client = None  # Initialize client to avoid UnboundLocalError
    try:
        client = await AsyncClient.create(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY)
        bm = BinanceSocketManager(client)
        socket = bm.kline_socket(symbol, interval="1m")

        async with socket as stream:
            while not stop_event.is_set():
                try:
                    msg = await stream.recv()
                    if msg['e'] == 'kline' and msg['k']['x']:
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
                        logger.info(f"Saved {symbol} price data")
                except Exception as e:
                    logger.error(f"Error processing message for {symbol}: {e}")
    except Exception as e:
        logger.error(f"Error in fetch_binance_data for {symbol}: {e}")
    finally:
        if client:  # Ensure client is defined before closing
            await client.close_connection()