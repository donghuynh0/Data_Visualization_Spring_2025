# Binance Price Data Fetcher

## Description
This Python script fetches 1-minute kline data for Bitcoin (BTCUSDT) and Ethereum (ETHUSDT) from the Binance API and saves it to separate CSV files. It uses the `binance` library for interacting with the API and `asyncio` for asynchronous operations, allowing it to fetch data for both symbols concurrently.

## Requirements
- Python 3.7 or higher
- `python-dotenv`
- `binance`
- `pandas`
- `pytz`

## Installation
1. Clone this repository.
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Create a `.env` file in the project root directory and add your Binance API key and secret:
    ```plaintext
    BINANCE_API_KEY=your_api_key
    BINANCE_SECRET_KEY=your_api_secret
    BTC_FILE_PATH=./btc_prices.csv
    ETH_FILE_PATH=./eth_prices.csv
    ```

## Usage
Run the script:
```bash
python main.py
```

The script will continuously fetch data for BTCUSDT and ETHUSDT and append it to `btc_prices.csv` and `eth_prices.csv` respectively. To stop the script, press `Ctrl+C`.

## Files
- `main.py`: Main script that fetches data from the Binance API and saves it to CSV files.
- `config.py`: Configuration file that loads environment variables.
- `data_fetcher.py`: Contains functions for fetching data from the Binance API.
- `logging_config.py`: Contains logging configuration.

## License
This project is licensed under the MIT License.