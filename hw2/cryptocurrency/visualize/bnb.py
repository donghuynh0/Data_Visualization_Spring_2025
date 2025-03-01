import os
import subprocess
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from flask import Flask
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dotenv import load_dotenv
import time

load_dotenv()

btc_file_path = os.getenv("BTC_FILE_PATH")
eth_file_path = os.getenv("ETH_FILE_PATH")
repo_path = os.getenv("REPO_PATH")  # Path to your Git repository

# Debug: Print repository path
print(f"Repository path: {repo_path}")

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Store the last update time
last_update_time = time.time()

def update_repository():
    """Pull the latest data from the Git repository"""
    global last_update_time
    if not repo_path or not os.path.exists(repo_path):
        print(f"❌ Repository path '{repo_path}' does not exist.")
        return False
    try:
        result = subprocess.run(["git", "pull"], cwd=repo_path, check=True, text=True, capture_output=True)
        print("✅ Git repository updated successfully.")
        print(result.stdout)
        last_update_time = time.time()  # Update the last update time
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git pull failed: {e.stderr}")
        return False

def get_latest_data(file_path):
    """Pull latest data from Git and read CSV file"""
    if update_repository():  # Pull latest data before reading
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            if not df.empty:
                df["Time"] = pd.to_datetime(df["Time"])
                return df
    return pd.DataFrame()

app.layout = html.Div([
    html.Div([
        html.H1("📊 Crypto Candlestick Chart", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id="coin-selector",
            options=[
                {"label": "Bitcoin (BTC/USDT)", "value": "BTCUSDT"},
                {"label": "Ethereum (ETH/USDT)", "value": "ETHUSDT"}
            ],
            value="BTCUSDT",
            clearable=False,
            style={
                "width": "190px",  
                "font-size": "16px",
                "margin": "10px",  
            },
            className="dropdown-container"
        ),
        dcc.Dropdown(
            id="timeframe-selector",
            options=[
                {"label": "1 Minute", "value": "1Min"},
                {"label": "15 Minutes", "value": "15Min"},
                {"label": "1 Hour", "value": "1H"},
                {"label": "4 Hours", "value": "4H"}
            ],
            value="1Min",
            clearable=False,
            style={
                "width": "190px",  
                "font-size": "16px",
                "margin": "10px",  
            }
        )
    ], style={"position": "relative", "display": "flex", "justify-content": "center"}),
    
    dcc.Graph(id="candlestick-chart", style={"margin-top": "-20px"}),

    dcc.Interval(
        id="interval-component",
        interval=10 * 1000,  # 10 seconds
        n_intervals=0
    ),

    # Store the last update time
    dcc.Store(id="last-update-time", data=last_update_time),

    # Hidden div to trigger a page refresh
    html.Div(id="refresh-page", style={"display": "none"})
])

@app.callback(
    [Output("candlestick-chart", "figure"),
     Output("last-update-time", "data"),
     Output("refresh-page", "children", allow_duplicate=True)],  # Allow duplicate output
    [Input("coin-selector", "value"),
     Input("timeframe-selector", "value"),
     Input("interval-component", "n_intervals")],
    [State("last-update-time", "data")],
    prevent_initial_call=True  # Prevent initial call for this callback
)
def update_candlestick_chart(symbol, timeframe, n_intervals, last_update):
    global last_update_time

    # Check if the interval triggered the callback
    if n_intervals > 0:  # Only proceed if the interval has triggered the callback
        if last_update_time > last_update:
            # Force a page refresh by returning a dummy value to the hidden div
            return go.Figure(), last_update_time, "refresh"

    # Proceed with updating the chart
    file_path = btc_file_path if symbol == "BTCUSDT" else eth_file_path
    df = get_latest_data(file_path)

    if not df.empty:
        resample_rule = {
            "1Min": "1Min",
            "15Min": "15Min",
            "1H": "1H",
            "4H": "4H"
        }[timeframe]
        df_resampled = df.resample(resample_rule, on="Time").agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })
        df_resampled.reset_index(inplace=True)

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.8, 0.2], vertical_spacing=0.05)

        fig.add_trace(go.Candlestick(
            x=df_resampled["Time"],
            open=df_resampled["Open"],
            high=df_resampled["High"],
            low=df_resampled["Low"],
            close=df_resampled["Close"],
            name=f"{symbol} Price"
        ), row=1, col=1)

        fig.add_trace(go.Bar(
            x=df_resampled["Time"],
            y=df_resampled["Volume"],
            marker_color=["green" if df_resampled["Close"].iloc[i] >= df_resampled["Open"].iloc[i] else "red" for i in range(len(df_resampled))],
            name="Volume"
        ), row=2, col=1)

        fig.update_layout(
            height=700,
            width=1500,
            xaxis_title="Time",
            yaxis_title="Price (USDT)",
            xaxis2_title="Time",
            xaxis=dict(rangeslider=dict(visible=False), tickangle=-15),
            showlegend=False
        )
        return fig, last_update_time, ""

    return go.Figure(), last_update_time, ""

# Add a callback to trigger a page refresh
app.clientside_callback(
    """
    function(refresh) {
        if (refresh === "refresh") {
            window.location.reload();
        }
    }
    """,
    Output("refresh-page", "children", allow_duplicate=True),  # Allow duplicate output
    Input("refresh-page", "children"),
    prevent_initial_call=True  # Prevent initial call for this callback
)

if __name__ == "__main__":
    app.run_server(debug=True)