import yfinance as yf
import pandas as pd

def get_options_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        
        # Get the nearest expiration date
        expirations = stock.options
        if not expirations:
            return None
        
        nearest_expiration = expirations[0]
        
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
