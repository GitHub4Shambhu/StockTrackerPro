import streamlit as st
import pandas as pd
from stock_data import get_stock_data
from options_data import get_options_data
from visualization import plot_stock_chart

st.set_page_config(
    page_title="Stock & Options Analyzer",
    page_icon="assets/favicon.svg",
    layout="wide"
)

st.title("Stock & Options Data Visualization")

# User input for stock symbol
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL):", "AAPL").upper()

if st.button("Analyze"):
    # Fetch stock data
    stock_data = get_stock_data(symbol)
    
    if stock_data is not None:
        # Display stock information
        st.subheader(f"{symbol} Stock Information")
        st.dataframe(stock_data)
        
        # Plot stock chart
        st.subheader(f"{symbol} Stock Price History")
        fig = plot_stock_chart(symbol)
        st.plotly_chart(fig, use_container_width=True)
        
        # Fetch options data
        options_data = get_options_data(symbol)
        
        if options_data is not None:
            # Display options data
            st.subheader(f"{symbol} Options Data")
            st.dataframe(options_data)
            
            # Combine stock and options data for CSV download
            combined_data = pd.concat([stock_data, options_data], axis=1)
            
            # CSV download button
            csv = combined_data.to_csv(index=False)
            st.download_button(
                label="Download Data as CSV",
                data=csv,
                file_name=f"{symbol}_stock_options_data.csv",
                mime="text/csv",
            )
        else:
            st.error("Unable to fetch options data. Please try again.")
    else:
        st.error("Unable to fetch stock data. Please check the symbol and try again.")

st.sidebar.markdown("""
## How to use this app:
1. Enter a valid stock symbol (e.g., AAPL for Apple Inc.)
2. Click the 'Analyze' button to fetch and display data
3. View the stock information table and price history chart
4. Explore the options data table
5. Download all data as a CSV file using the button below the tables
""")
