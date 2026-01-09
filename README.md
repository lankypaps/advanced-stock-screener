# Advanced Growth Stock Screener

A professional-grade Streamlit web application for screening stocks based on revenue and earnings growth metrics. Get real-time financial data and identify growth opportunities across global stock exchanges.

## Features

✨ **Core Features**
- Filter stocks by customizable revenue and earnings growth thresholds
- Analyze multiple tickers across different exchanges (US, UK, Germany, Canada, etc.)
- Real-time market data and financial metrics
- Conditional formatting for easy insight identification
- Download results as CSV for further analysis

🎯 **Advanced Features**
- Progress tracking during analysis
- Summary statistics (total analyzed, matches found, average growth)
- Session state for saving ticker lists
- Pre-configured popular stock lists (FTSE 100, US Tech)
- Error handling with detailed error reporting
- Wide responsive layout

## Installation

### Requirements
- Python 3.8+
- pip

### Setup

```bash
git clone https://github.com/lankypaps/advanced-stock-screener.git
cd advanced-stock-screener
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

### How to Use

1. **Set Growth Thresholds** - Adjust minimum revenue and earnings growth in the sidebar
2. **Select Stocks** - Enter ticker symbols (comma-separated)
3. **Load Presets** - Or click "Load FTSE 100 Sample" or "Load US Tech Sample" buttons
4. **Analyze** - Click "Screen Stocks" to fetch and analyze data
5. **Review Results** - Sort, filter, and download results

### Ticker Format Examples

- **US Stocks**: `AAPL`, `MSFT`, `GOOGL`, `AMZN`
- **UK Stocks (LSE)**: `BP..L`, `SHEL.L`, `HSBA.L`, `AZN.L`
- **German Stocks**: `BMW.DE`, `SAP.DE`, `SIE.DE`
- **Canadian Stocks**: `RY.TO`, `TD.TO`, `BN.TO`

## Features Explained

### Revenue & Earnings Growth
- **Revenue Growth**: Year-over-year percentage change in total revenue
- **Earnings Growth**: Year-over-year percentage change in net income
- Green highlighting indicates stocks meeting your criteria

### Market Metrics
- **Market Cap**: Company valuation in billions
- **P/E Ratio**: Price-to-earnings ratio for valuation context
- **Sector**: Industry classification

## Limitations

- Data availability varies by stock and exchange
- Some stocks may have incomplete financial history
- Yahoo Finance API rate limits may apply for large batches
- Financial data may be delayed by 1-2 business days

## Data Source

Data is provided by [Yahoo Finance](https://finance.yahoo.com/) via the [yfinance](https://github.com/ranaroussi/yfinance) Python library.

## Disclaimer

**This tool is for informational purposes only and is not financial advice.** Please consult with a qualified financial advisor before making investment decisions. Past performance does not guarantee future results.

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
