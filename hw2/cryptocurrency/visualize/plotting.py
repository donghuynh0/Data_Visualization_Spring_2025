import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_candlestick_chart(df, symbol):
    """Create a candlestick chart with moving averages, volume, and a legend."""
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.8, 0.2],  
        vertical_spacing=0.05
    )

    # Candlestick Chart
    fig.add_trace(go.Candlestick(
        x=df["Time"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name=f"{symbol} Price"
    ), row=1, col=1)

    # Moving Averages 
    fig.add_trace(go.Scatter(
        x=df["Time"],
        y=df["MA_7"],
        line=dict(color="blue", width=1.5),
        name="MA 7",
        mode="lines"  
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df["Time"],
        y=df["MA_25"],
        line=dict(color="orange", width=1.5),
        name="MA 25",
        mode="lines" 
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df["Time"],
        y=df["MA_99"],
        line=dict(color="purple", width=1.5),
        name="MA 99",
        mode="lines"  
    ), row=1, col=1)

    # Volume Chart
    fig.add_trace(go.Bar(
        x=df["Time"],
        y=df["Volume"],
        marker_color=["green" if df["Close"].iloc[i] >= df["Open"].iloc[i] else "red" for i in range(len(df))],
        name="Volume"
    ), row=2, col=1)

    fig.update_layout(
        height=700,
        width=1500,
        yaxis_title="Price (USDT)",
        xaxis2_title="Time",
        xaxis=dict(rangeslider=dict(visible=False), tickangle=-15),
        showlegend=True,  
        legend=dict(
            x=1.02,  
            y=1, 
            xanchor="left",  
            yanchor="top", 
            bgcolor="rgba(255, 255, 255, 0.5)", 
        ),
        margin=dict(l=50, r=150, t=50, b=50)  
    )

    return fig