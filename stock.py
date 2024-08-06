import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

COMPANY_TICKERS = {
    'Apple': 'AAPL',
    'Google': 'GOOGL',
    'Microsoft': 'MSFT',
    'Amazon': 'AMZN',
    'Facebook': 'META',
    'Tesla': 'TSLA',
    'Netflix': 'NFLX',
    'NVIDIA': 'NVDA',
    'Uber': 'UBER'
}

def get_stock_data(tickers, period='1mo'):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        data[ticker] = hist
    return data

st.set_page_config(layout="wide")

st.title('Live Stock Price Dashboard')


st.sidebar.header('User Input')
selected_companies = st.sidebar.multiselect('Select Companies', list(COMPANY_TICKERS.keys()), ['Apple', 'Google', 'Microsoft'])
period = st.sidebar.selectbox('Select Period', ['1mo', '3mo', '6mo', '1y', '2y', '5y'])
moving_avg_days = st.sidebar.slider('Select Moving Average Days', min_value=5, max_value=50, value=20, step=5)

if selected_companies:
    ticker_list = [COMPANY_TICKERS[company] for company in selected_companies]
    data = get_stock_data(ticker_list, period)
    
    for ticker in ticker_list:
        stock_data = data[ticker]
        
        st.header(f'{ticker} Stock Data')
        
        col1, col2 = st.columns(2)
        
        
        with col1:
            st.subheader('Closing Price')
            st.line_chart(stock_data['Close'])
     
        with col2:
            st.subheader('Volume')
            st.bar_chart(stock_data['Volume'])
        

        stock_data[f'{moving_avg_days}-Day MA'] = stock_data['Close'].rolling(window=moving_avg_days).mean()
        st.subheader(f'{moving_avg_days}-Day Moving Average')
        st.line_chart(stock_data[['Close', f'{moving_avg_days}-Day MA']])
        

        stock_data['Middle Band'] = stock_data['Close'].rolling(window=moving_avg_days).mean()
        stock_data['Upper Band'] = stock_data['Middle Band'] + 2*stock_data['Close'].rolling(window=moving_avg_days).std()
        stock_data['Lower Band'] = stock_data['Middle Band'] - 2*stock_data['Close'].rolling(window=moving_avg_days).std()
        st.subheader('Bollinger Bands')
        st.line_chart(stock_data[['Close', 'Upper Band', 'Middle Band', 'Lower Band']])
        
       
        st.subheader('Candlestick Chart')
        fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                             open=stock_data['Open'],
                                             high=stock_data['High'],
                                             low=stock_data['Low'],
                                             close=stock_data['Close'])])
        st.plotly_chart(fig)
        
      
        st.subheader('Key Metrics')
        key_metrics = yf.Ticker(ticker).info
        st.write(f"Market Cap: {key_metrics['marketCap']:,}")
        st.write(f"52-Week High: {key_metrics['fiftyTwoWeekHigh']}")
        st.write(f"52-Week Low: {key_metrics['fiftyTwoWeekLow']}")
        st.write(f"Volume: {key_metrics['volume']:,}")
        st.write(f"Previous Close: {key_metrics['previousClose']}")


    st.header('Comparison Charts')
    
    
    closing_prices = pd.DataFrame({ticker: data[ticker]['Close'] for ticker in ticker_list})
    st.subheader('Closing Prices Comparison')
    st.line_chart(closing_prices)
    
   
    volumes = pd.DataFrame({ticker: data[ticker]['Volume'] for ticker in ticker_list})
    st.subheader('Volumes Comparison')
    st.bar_chart(volumes)
    
    
    moving_averages = pd.DataFrame({ticker: data[ticker]['Close'].rolling(window=moving_avg_days).mean() for ticker in ticker_list})
    st.subheader(f'{moving_avg_days}-Day Moving Averages Comparison')
    st.line_chart(moving_averages)
    
    
    st.subheader('Daily Returns Comparisons')
    daily_returns = closing_prices.pct_change().dropna()
    st.line_chart(daily_returns)

   


        
        