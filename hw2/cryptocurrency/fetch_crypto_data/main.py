import asyncio
from config import btc_file_path, eth_file_path
from data_fetcher import fetch_binance_data
from logging_config import get_logger

logger = get_logger(__name__)

async def main():
    stop_event = asyncio.Event()
    try:
        await asyncio.gather(
            fetch_binance_data("BTCUSDT", btc_file_path, stop_event),
            fetch_binance_data("ETHUSDT", eth_file_path, stop_event)
        )
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
        stop_event.set()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())