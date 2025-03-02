import os
import pandas as pd

def get_latest_data(file_path, last_update_time):
    # read CSV file and return new data since the last update.
    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            if not df.empty:
                df["Time"] = pd.to_datetime(df["Time"])
                df = df[df["Time"] > pd.to_datetime(last_update_time, unit="s")]
                return df
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return pd.DataFrame()

def resample_data(df, timeframe):
    # resample data based on the selected timeframe.
    resample_rule = {
        "1Min": "1Min",
        "15Min": "15Min",
        "1H": "1h",
        "4H": "4h"
    }[timeframe]
    
    df_resampled = df.resample(resample_rule, on="Time").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    })
    df_resampled.reset_index(inplace=True)
    return df_resampled

def calculate_moving_averages(df):
    # calculate moving averages 
    df["MA_7"] = df["Close"].rolling(window=7, min_periods=1).mean()
    df["MA_25"] = df["Close"].rolling(window=25, min_periods=1).mean()
    df["MA_99"] = df["Close"].rolling(window=99, min_periods=1).mean()
    return df