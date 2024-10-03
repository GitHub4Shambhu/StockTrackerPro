import streamlit as st
import pandas as pd
from stock_data import get_stock_data
from options_data import get_options_data
from visualization import plot_stock_chart, plot_comparison_chart

st.set_page_config(
    page_title="Stock & Options Analyzer",
    page_icon="assets/favicon.svg",
    layout="wide"
)

st.title("Stock & Options Data Visualization")

# User input for multiple stock symbols
symbols = st.text_input("Enter Stock Symbols (comma-separated, e.g., AAPL,GOOGL,MSFT):", "AAPL,GOOGL,MSFT").upper().split(',')
symbols = [symbol.strip() for symbol in symbols]

if st.button("Analyze"):
    # Fetch stock data for all symbols
    stock_data_list = []
    for symbol in symbols:
        data = get_stock_data(symbol)
        if data is not None:
            stock_data_list.append(data)

    if stock_data_list:
        # Combine stock data for all symbols
        combined_stock_data = pd.concat(stock_data_list, ignore_index=True)

        # Display combined stock information
        st.subheader("Stock Information Comparison")
        st.dataframe(combined_stock_data)

        # Plot comparison chart
        st.subheader("Stock Price Comparison")
        fig = plot_comparison_chart(symbols)
        st.plotly_chart(fig, use_container_width=True)

        # Display individual stock charts with technical indicators
        for symbol in symbols:
            st.subheader(f"{symbol} Stock Price History and Technical Indicators")
            fig = plot_stock_chart(symbol)
            st.plotly_chart(fig, use_container_width=True)

        # Fetch and display options data for each symbol
        for symbol in symbols:
            options_data = get_options_data(symbol)
            if options_data is not None:
                st.subheader(f"{symbol} Options Data")
                st.dataframe(options_data)

        # Combine all data for CSV download
        all_data = [combined_stock_data]
        for symbol in symbols:
            options_data = get_options_data(symbol)
            if options_data is not None:
                all_data.append(options_data)

        combined_data = pd.concat(all_data, keys=symbols)

        # CSV download button
        csv = combined_data.to_csv(index=True)
        st.download_button(
            label="Download All Data as CSV",
            data=csv,
            file_name="stock_options_comparison_data.csv",
            mime="text/csv",
        )
    else:
        st.error("Unable to fetch stock data. Please check the symbols and try again.")

st.sidebar.markdown("""
## How to use this app:
1. Enter valid stock symbols separated by commas (e.g., AAPL,GOOGL,MSFT)
2. Click the 'Analyze' button to fetch and display data
3. View the stock information comparison table
4. Explore the stock price comparison chart
5. Check individual stock price history charts with technical indicators:
   - Candlestick chart
   - 20-day and 50-day Moving Averages
   - Relative Strength Index (RSI)
   - Volume
6. Review options data for each stock
7. Download all data as a CSV file using the button below the tables
""")
