import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📈 Growth Stock Screener")
st.write("Filter stocks based on revenue and earnings growth metrics")

# Sidebar for criteria
st.sidebar.header("Screening Criteria")
min_revenue_growth = st.sidebar.number_input("Min Revenue Growth (%)", value=15.0)
min_earnings_growth = st.sidebar.number_input("Min Earnings Growth (%)", value=10.0)

# Input tickers
tickers_input = st.text_input("Enter stock tickers (comma-separated)", "AAPL,MSFT,GOOGL,NVDA")

if st.button("Screen Stocks"):
    tickers = [t.strip() for t in tickers_input.split(",")]
    results = []
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            financials = stock.financials
            
            # Calculate growth metrics from financial data
            revenue_growth = 0
            earnings_growth = 0
            
            if len(financials) >= 2:
                recent_revenue = financials.iloc[0]['Total Revenue'] if 'Total Revenue' in financials.index else 0
                prior_revenue = financials.iloc[1]['Total Revenue'] if 'Total Revenue' in financials.index else 0
                if prior_revenue > 0:
                    revenue_growth = ((recent_revenue - prior_revenue) / prior_revenue) * 100
                
                recent_earnings = financials.iloc[0]['Net Income'] if 'Net Income' in financials.index else 0
                prior_earnings = financials.iloc[1]['Net Income'] if 'Net Income' in financials.index else 0
                if prior_earnings > 0:
                    earnings_growth = ((recent_earnings - prior_earnings) / prior_earnings) * 100
            
            results.append({
                'Ticker': ticker,
                'Revenue Growth': round(revenue_growth, 2),
                'Earnings Growth': round(earnings_growth, 2),
                'Market Cap': round(info.get('marketCap', 0) / 1e9, 2)
            })
        except Exception as e:
            st.warning(f"Could not fetch data for {ticker}: {str(e)}")
    
    df = pd.DataFrame(results)
    # Filter based on criteria
    df_filtered = df[(df['Revenue Growth'] >= min_revenue_growth) & 
                     (df['Earnings Growth'] >= min_earnings_growth)]
    
    st.dataframe(df_filtered)
