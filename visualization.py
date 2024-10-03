import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
import numpy as np

def calculate_ma(data, window):
    return data['Close'].rolling(window=window).mean()

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def plot_stock_chart(symbol):
    # Fetch historical data
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1y")
    
    # Calculate technical indicators
    hist['MA20'] = calculate_ma(hist, 20)
    hist['MA50'] = calculate_ma(hist, 50)
    hist['RSI'] = calculate_rsi(hist)
    
    # Create the candlestick chart
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name='Candlestick'))
    
    # Add Moving Averages
    fig.add_trace(go.Scatter(x=hist.index, y=hist['MA20'], name='20-day MA', line=dict(color='blue', width=1)))
    fig.add_trace(go.Scatter(x=hist.index, y=hist['MA50'], name='50-day MA', line=dict(color='red', width=1)))
    
    # Add volume bars
    fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume', yaxis='y2', marker_color='rgba(0,0,255,0.3)'))
    
    # Add RSI
    fig.add_trace(go.Scatter(x=hist.index, y=hist['RSI'], name='RSI', yaxis='y3', line=dict(color='purple', width=1)))
    
    # Update layout
    fig.update_layout(
        title=f'{symbol} Stock Price, Volume, and Technical Indicators',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        yaxis2=dict(
            title='Volume',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue'),
            anchor='x',
            overlaying='y',
            side='right'
        ),
        yaxis3=dict(
            title='RSI',
            titlefont=dict(color='purple'),
            tickfont=dict(color='purple'),
            anchor='x',
            overlaying='y',
            side='right'
        ),
        height=800
    )
    
    # Add RSI levels
    fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=3, col=1)
    
    return fig

def plot_comparison_chart(symbols):
    fig = go.Figure()

    for symbol in symbols:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1y")
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name=symbol))

    fig.update_layout(
        title='Stock Price Comparison',
        xaxis_title='Date',
        yaxis_title='Closing Price',
        legend_title='Symbols',
        height=600
    )

    return fig
