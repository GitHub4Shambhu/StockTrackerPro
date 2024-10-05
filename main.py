import streamlit as st
import pandas as pd
from datetime import date, timedelta
from stock_data import get_stock_data
from options_data import get_options_data
from visualization import plot_stock_chart, plot_comparison_chart
from news_sentiment import get_news_sentiment

# Add custom CSS
def load_css():
    with open(".streamlit/styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.set_page_config(
    page_title="Stock & Options Analyzer",
    page_icon="assets/favicon.svg",
    layout="wide"
)

# Load custom CSS
load_css()

st.title("Stock & Options Data Visualization")

# User input for multiple stock symbols
symbols = st.text_input("Enter Stock Symbols (comma-separated, e.g., AAPL,GOOGL,MSFT):", "AAPL,GOOGL,MSFT").upper().split(',')
symbols = [symbol.strip() for symbol in symbols]

# Date range selection
st.subheader("Select Date Range")
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", date.today() - timedelta(days=365))
with col2:
    end_date = st.date_input("End Date", date.today())

if st.button("Analyze"):
    # Fetch stock data for all symbols
    stock_data_list = []
    for symbol in symbols:
        data = get_stock_data(symbol, start_date, end_date)
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
        fig = plot_comparison_chart(symbols, start_date, end_date)
        st.plotly_chart(fig, use_container_width=True)

        # Display individual stock charts with technical indicators and news sentiment
        for symbol in symbols:
            st.subheader(f"{symbol} Stock Analysis")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Price History and Technical Indicators")
                fig = plot_stock_chart(symbol, start_date, end_date)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("News Sentiment Analysis")
                news_sentiment = get_news_sentiment(symbol)
                if news_sentiment is not None:
                    st.write(f"Average Sentiment: {news_sentiment['sentiment'].mean():.2f}")
                    st.bar_chart(news_sentiment['sentiment_category'].value_counts())
                    st.dataframe(news_sentiment[['title', 'sentiment_category', 'url']])
                else:
                    st.write("Unable to fetch news sentiment data.")

        # Fetch and display options data for each symbol
        for symbol in symbols:
            options_data = get_options_data(symbol, end_date)
            if options_data is not None:
                st.subheader(f"{symbol} Options Data")
                st.dataframe(options_data)

        # Combine all data for CSV download
        all_data = [combined_stock_data]
        for symbol in symbols:
            options_data = get_options_data(symbol, end_date)
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
2. Select the desired date range for historical data
3. Click the 'Analyze' button to fetch and display data
4. View the stock information comparison table
5. Explore the stock price comparison chart
6. Check individual stock analysis:
   - Price history chart with technical indicators
   - News sentiment analysis
7. Review options data for each stock
8. Download all data as a CSV file using the button below the tables
""")
