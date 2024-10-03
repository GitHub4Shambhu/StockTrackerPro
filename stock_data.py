import yfinance as yf
import pandas as pd

def get_stock_data(symbol, start_date, end_date):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(start=start_date, end=end_date)
        
        if hist.empty:
            return None
        
        latest_data = hist.iloc[-1]
        
        # Extract relevant information
        data = {
            "Symbol": symbol,
            "Company Name": stock.info.get("longName", "N/A"),
            "Current Price": latest_data['Close'],
            "Previous Close": hist.iloc[-2]['Close'] if len(hist) > 1 else "N/A",
            "Open": latest_data['Open'],
            "Day's Range": f"{latest_data['Low']} - {latest_data['High']}",
            "52 Week Range": f"{hist['Low'].min()} - {hist['High'].max()}",
            "Market Cap": stock.info.get("marketCap", "N/A"),
            "Volume": latest_data['Volume'],
            "Avg. Volume": hist['Volume'].mean(),
            "P/E Ratio": stock.info.get("trailingPE", "N/A"),
            "EPS": stock.info.get("trailingEps", "N/A"),
            "Dividend Yield": stock.info.get("dividendYield", "N/A"),
            "Beta": stock.info.get("beta", "N/A"),
        }
        
        return pd.DataFrame([data])
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None
