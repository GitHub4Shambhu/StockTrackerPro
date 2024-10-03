import yfinance as yf
import plotly.graph_objs as go

def plot_stock_chart(symbol):
    # Fetch historical data
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1y")
    
    # Create the candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'])])
    
    # Add volume bars
    fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume', yaxis='y2', marker_color='rgba(0,0,255,0.3)'))
    
    # Update layout
    fig.update_layout(
        title=f'{symbol} Stock Price and Volume',
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
        height=600
    )
    
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
