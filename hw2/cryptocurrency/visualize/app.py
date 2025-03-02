import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import time
from flask import Flask
import plotly.graph_objects as go
from config import btc_file_path, eth_file_path
from data_processing import get_latest_data, resample_data, calculate_moving_averages
from plotting import create_candlestick_chart
server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# App layout
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id="coin-selector",
            options=[
                {"label": "Bitcoin (BTC/USDT)", "value": "BTCUSDT"},
                {"label": "Ethereum (ETH/USDT)", "value": "ETHUSDT"}
            ],
            value="BTCUSDT",
            clearable=False,
            style={"width": "190px", "font-size": "16px", "margin": "10px"},
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
            style={"width": "190px", "font-size": "16px", "margin": "10px"}
        )
    ], style={"position": "relative", "display": "flex", "justify-content": "center"}),
    
    dcc.Loading(
        id="loading",
        type="circle",
        children=[dcc.Graph(id="candlestick-chart", style={"margin-top": "-20px"})]
    ),

    dcc.Interval(
        id="interval-component",
        interval=60 * 1000,  # 60 seconds
        n_intervals=0
    ),

    dcc.Store(id="last-update-time", data=time.time()),
    html.Div(id="refresh-page", style={"display": "none"})
])

@app.callback(
    [Output("candlestick-chart", "figure"),
     Output("last-update-time", "data"),
     Output("refresh-page", "children")],
    [Input("coin-selector", "value"),
     Input("timeframe-selector", "value"),
     Input("interval-component", "n_intervals")],
    [State("last-update-time", "data")],
    prevent_initial_call=True
)
def update_candlestick_chart(symbol, timeframe, n_intervals, last_update):
    file_path = btc_file_path if symbol == "BTCUSDT" else eth_file_path
    df = get_latest_data(file_path, last_update)

    if not df.empty:
        df_resampled = resample_data(df, timeframe)
        df_resampled = calculate_moving_averages(df_resampled)
        fig = create_candlestick_chart(df_resampled, symbol)
        return fig, time.time(), "refresh"
    else:
        # No new data, do not refresh
        return go.Figure(), last_update, ""

if __name__ == "__main__":
    app.run_server(debug=True)