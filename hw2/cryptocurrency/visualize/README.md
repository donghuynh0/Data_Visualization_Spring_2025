# Cryptocurrency Visualization

## Description
This project visualizes cryptocurrency data using Dash and Plotly. It includes a candlestick chart with moving averages and volume for Bitcoin (BTC/USDT) and Ethereum (ETH/USDT). The data is fetched from CSV files and updated at regular intervals.

## Requirements
- Python 3.7 or higher
- `dash`
- `plotly`
- `pandas`
- `python-dotenv`
- `flask`

## Installation
1. Clone this repository.
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Create a `.env` file in the project root directory and add the paths to your CSV files:
    ```plaintext
    BTC_FILE_PATH=./btc_prices.csv
    ETH_FILE_PATH=./eth_prices.csv
    ```

## Usage
Run the Dash app:
```bash
python app.py
```

The app will start a local server and open a web page displaying the candlestick chart. The chart will update every minute with the latest data from the CSV files.

## Files
- `app.py`: Main application file that sets up the Dash app and its layout.
- `config.py`: Configuration file that loads environment variables.
- `data_processing.py`: Contains functions for reading and processing the data.
- `plotting.py`: Contains functions for creating the candlestick chart.

## License
This project is licensed under the MIT License.
