import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Flask
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dotenv import load_dotenv

load_dotenv()

btc_file_path = os.getenv("BTC_FILE_PATH")
eth_file_path = os.getenv("ETH_FILE_PATH")

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

def get_latest_data(file_path):
    """Read all available price data from CSV file"""
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
            value="1Min",  # Default timeframe
            clearable=False,
            style={
                "width": "190px",  
                "font-size": "16px",
                "margin": "10px",  
            }
        )
    ], style={"position": "relative", "display": "flex", "justify-content": "center"}),
    
    dcc.Graph(id="candlestick-chart", style={"margin-top": "-20px"})
])

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

@app.callback(
    Output("candlestick-chart", "figure"),
    [Input("coin-selector", "value"),
     Input("timeframe-selector", "value")]
)
def update_candlestick_chart(symbol, timeframe):
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
        return fig

    return go.Figure()

if __name__ == "__main__":
    app.run_server(debug=True)