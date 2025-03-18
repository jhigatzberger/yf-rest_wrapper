
import yfinance as yf
ticker_obj = yf.Ticker("AAPL")
financials = ticker_obj.financials

print(financials)