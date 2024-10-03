import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_options_data(symbol, end_date):
    try:
        stock = yf.Ticker(symbol)
        
        # Get the nearest expiration date after the end_date
        expirations = [date for date in stock.options if datetime.strptime(date, "%Y-%m-%d").date() >= end_date]
        if not expirations:
            return None
        
        nearest_expiration = min(expirations)
        
        # Fetch both call and put options
        calls = stock.option_chain(nearest_expiration).calls
        puts = stock.option_chain(nearest_expiration).puts
        
        # Combine calls and puts
        options = pd.concat([calls, puts])
        
        # Select relevant columns
        columns = ['contractSymbol', 'strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest', 'impliedVolatility']
        options = options[columns]
        
        # Rename columns for clarity
        options.columns = ['Contract', 'Strike', 'Last Price', 'Bid', 'Ask', 'Volume', 'Open Interest', 'Implied Volatility']
        
        # Sort by strike price
        options = options.sort_values('Strike')
        
        return options
    except Exception as e:
        print(f"Error fetching options data: {e}")
        return None
