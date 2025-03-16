from flask import Flask, jsonify
import yfinance as yf

app = Flask(__name__)

# General ticker data
@app.route('/stock/<string:ticker>', methods=['GET'])
def ticker_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return jsonify(info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Growth estimates
@app.route('/stock/<string:ticker>/growth_estimates', methods=['GET'])
def growth_estimates(ticker):
    try:
        stock = yf.Ticker(ticker)
        growth = stock.growth_estimates
        return growth.to_json(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Earnings data
@app.route('/stock/<string:ticker>/earnings', methods=['GET'])
def earnings(ticker):
    try:
        stock = yf.Ticker(ticker)
        earnings = stock.earnings
        return earnings.to_json(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Balance sheet
@app.route('/stock/<string:ticker>/balance_sheet', methods=['GET'])
def balance_sheet(ticker):
    try:
        stock = yf.Ticker(ticker)
        bs = stock.balance_sheet
        return bs.to_json(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Income statement
@app.route('/stock/<string:ticker>/income_stmt', methods=['GET'])
def income_stmt(ticker):
    try:
        stock = yf.Ticker(ticker)
        inc_stmt = stock.income_stmt
        return inc_stmt.to_json(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Cashflow
@app.route('/stock/<string:ticker>/cashflow', methods=['GET'])
def cashflow(ticker):
    try:
        stock = yf.Ticker(ticker)
        cf = stock.cashflow
        return cf.to_json(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Dividends
@app.route('/stock/<string:ticker>/dividends', methods=['GET'])
def dividends(ticker):
    try:
        stock = yf.Ticker(ticker)
        dividends = stock.dividends
        return dividends.to_json(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Splits
@app.route('/stock/<string:ticker>/splits', methods=['GET'])
def splits(ticker):
    try:
        stock = yf.Ticker(ticker)
        splits = stock.splits
        return splits.to_json(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Institutional holders
@app.route('/stock/<string:ticker>/institutional_holders', methods=['GET'])
def institutional_holders(ticker):
    try:
        stock = yf.Ticker(ticker)
        holders = stock.institutional_holders
        return holders.to_json(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Explanation:

- Each endpoint is clearly separated, returning the relevant pandas DataFrame as JSON (`to_json()`).
- Error handling ensures you always return meaningful responses.

### Example usage:

- General info:
  ```
  GET /stock/AAPL
```
- Growth estimates:
  ```
  GET /stock/AAPL/growth_estimates
```
- Earnings:
  ```
  GET /stock/AAPL/earnings
```
- Balance Sheet:
  ```
  GET /stock/AAPL/balance_sheet
  ```

- Cashflow:
  ```
  GET /stock/AAPL/cashflow
  ```

Each endpoint directly corresponds to the functionality provided by the yfinance API, making the application easy to maintain and extend.