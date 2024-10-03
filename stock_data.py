import yfinance as yf
import pandas as pd

def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # Extract relevant information
        data = {
            "Symbol": symbol,
            "Company Name": info.get("longName", "N/A"),
            "Current Price": info.get("currentPrice", "N/A"),
            "Previous Close": info.get("previousClose", "N/A"),
            "Open": info.get("open", "N/A"),
            "Day's Range": f"{info.get('dayLow', 'N/A')} - {info.get('dayHigh', 'N/A')}",
            "52 Week Range": f"{info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}",
            "Market Cap": info.get("marketCap", "N/A"),
            "Volume": info.get("volume", "N/A"),
            "Avg. Volume": info.get("averageVolume", "N/A"),
            "P/E Ratio": info.get("trailingPE", "N/A"),
            "EPS": info.get("trailingEps", "N/A"),
            "Dividend Yield": info.get("dividendYield", "N/A"),
            "Beta": info.get("beta", "N/A"),
        }
        
        return pd.DataFrame([data])
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None
