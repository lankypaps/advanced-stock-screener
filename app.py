import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

st.set_page_config(page_title="Growth Stock Screener", page_icon="📈", layout="wide")

st.title("📈 Growth Stock Screener")
st.write("Filter stocks based on revenue and earnings growth metrics using real market data")

st.sidebar.header("Screening Criteria")
min_revenue_growth = st.sidebar.number_input(
    "Minimum Revenue Growth (%)", value=15.0, step=1.0,
    help="Year-over-year revenue growth threshold"
)
min_earnings_growth = st.sidebar.number_input(
    "Minimum Earnings Growth (%)", value=10.0, step=1.0,
    help="Year-over-year earnings growth threshold"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Popular Lists")
if st.sidebar.button("Load FTSE 100 Sample"):
    st.session_state['tickers'] = "BP..L,SHEL.L,HSBA.L,AZN.L,ULVR.L"
if st.sidebar.button("Load US Tech Sample"):
    st.session_state['tickers'] = "AAPL,MSFT,GOOGL,AMZN,NVDA"

default_tickers = st.session_state.get('tickers', "AAPL,MSFT,GOOGL")
tickers_input = st.text_area(
    "Enter stock tickers (comma-separated)", value=default_tickers, height=100,
    help="Use ticker symbols like: AAPL for US stocks, BP..L for UK stocks"
)

def calculate_growth_rate(values):
    if len(values) < 2:
        return None
    current = values.iloc[0]
    previous = values.iloc[1]
    if previous == 0 or pd.isna(previous) or pd.isna(current):
        return None
    growth = ((current - previous) / abs(previous)) * 100
    return round(growth, 2)

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        financials = stock.financials
        
        result = {
            'Ticker': ticker,
            'Company': info.get('longName', ticker),
            'Market Cap (B)': round(info.get('marketCap', 0) / 1e9, 2) if info.get('marketCap') else None,
            'P/E Ratio': round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else None,
            'Sector': info.get('sector', 'N/A'),
            'Revenue Growth (%)': None,
            'Earnings Growth (%)': None,
            'Error': None
        }
        
        if not financials.empty and 'Total Revenue' in financials.index:
            revenue_values = financials.loc['Total Revenue']
            result['Revenue Growth (%)'] = calculate_growth_rate(revenue_values)
        
        if not financials.empty and 'Net Income' in financials.index:
            earnings_values = financials.loc['Net Income']
            result['Earnings Growth (%)'] = calculate_growth_rate(earnings_values)
        
        rev_growth = result['Revenue Growth (%)']
        earn_growth = result['Earnings Growth (%)']
        
        result['Meets Criteria'] = (
            rev_growth is not None and earn_growth is not None and
            rev_growth >= min_revenue_growth and earn_growth >= min_earnings_growth
        )
        return result
    except Exception as e:
        return {
            'Ticker': ticker, 'Company': ticker, 'Market Cap (B)': None,
            'P/E Ratio': None, 'Sector': None, 'Revenue Growth (%)': None,
            'Earnings Growth (%)': None, 'Meets Criteria': False,
            'Error': str(e)[:100]
        }

def style_dataframe(df):
    def color_growth(val):
        if pd.isna(val):
            return ''
        color = 'green' if val >= 0 else 'red'
        return f'color: {color}; font-weight: bold'
    
    def highlight_meets_criteria(row):
        if row['Meets Criteria']:
            return ['background-color: #d4edda'] * len(row)
        return [''] * len(row)
    
    styled = df.style.map(
        color_growth, subset=['Revenue Growth (%)', 'Earnings Growth (%)']
    ).apply(highlight_meets_criteria, axis=1)
    return styled

if st.button("🔍 Screen Stocks", type="primary"):
    tickers = [t.strip() for t in tickers_input.split(",") if t.strip()]
    
    if not tickers:
        st.error("Please enter at least one ticker symbol")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        results = []
        
        for idx, ticker in enumerate(tickers):
            status_text.text(f"Analyzing {ticker}... ({idx + 1}/{len(tickers)})")
            result = get_stock_data(ticker)
            results.append(result)
            progress_bar.progress((idx + 1) / len(tickers))
            time.sleep(0.5)
        
        status_text.empty()
        progress_bar.empty()
        
        df = pd.DataFrame(results)
        df_success = df[df['Error'].isna()].copy()
        df_errors = df[df['Error'].notna()].copy()
        
        if not df_success.empty:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Analyzed", len(df_success))
            with col2:
                meets_criteria = df_success['Meets Criteria'].sum()
                st.metric("Growth Stocks Found", meets_criteria)
            with col3:
                avg_rev_growth = df_success['Revenue Growth (%)'].mean()
                st.metric("Avg Revenue Growth", f"{avg_rev_growth:.1f}%" if not pd.isna(avg_rev_growth) else "N/A")
            with col4:
                avg_earn_growth = df_success['Earnings Growth (%)'].mean()
                st.metric("Avg Earnings Growth", f"{avg_earn_growth:.1f}%" if not pd.isna(avg_earn_growth) else "N/A")
            
            st.markdown("---")
            show_all = st.checkbox("Show all stocks (not just those meeting criteria)", value=True)
            
            if not show_all:
                df_display = df_success[df_success['Meets Criteria']].copy()
                if df_display.empty:
                    st.warning(f"No stocks met criteria (Revenue ≥ {min_revenue_growth}%, Earnings ≥ {min_earnings_growth}%)")
                    df_display = df_success
            else:
                df_display = df_success
            
            df_display = df_display.sort_values('Revenue Growth (%)', ascending=False)
            st.subheader(f"Results ({len(df_display)} stocks)")
            
            display_cols = ['Ticker', 'Company', 'Sector', 'Market Cap (B)', 'P/E Ratio', 
                          'Revenue Growth (%)', 'Earnings Growth (%)', 'Meets Criteria']
            df_display = df_display[display_cols]
            
            st.dataframe(style_dataframe(df_display), use_container_width=True, height=400)
            
            csv = df_display.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name=f"growth_stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        if not df_errors.empty:
            with st.expander(f"⚠️ Failed to fetch data for {len(df_errors)} ticker(s)"):
                st.dataframe(df_errors[['Ticker', 'Error']], use_container_width=True)

with st.expander("ℹ️ How to Use & Tips"):
    st.markdown("""
    ### How It Works
    1. Set your minimum growth thresholds in the sidebar
    2. Enter stock tickers (comma-separated)
    3. Click "Screen Stocks" to analyze
    
    ### Ticker Format Examples
    - **US Stocks**: `AAPL`, `MSFT`, `GOOGL`
    - **UK Stocks (LSE)**: `BP..L`, `SHEL.L`, `HSBA.L`
    - **German Stocks**: `BMW.DE`, `SAP.DE`
    - **Canadian Stocks**: `RY.TO`, `TD.TO`
    
    ### About the Metrics
    - **Revenue Growth**: Year-over-year change in total revenue
    - **Earnings Growth**: Year-over-year change in net income
    - Growth stocks are highlighted in green
    """)

st.markdown("---")
st.caption("Data provided by Yahoo Finance via yfinance library. Not financial advice.")
