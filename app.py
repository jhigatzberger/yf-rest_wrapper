from flask import Flask, jsonify, request
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)

pd.options.mode.use_inf_as_na = True

def clean_json(df):
    # Replace literal strings "NaN" or "nan" with actual np.nan
    df = df.replace(["NaN", "nan"], np.nan)
    # Replace infinities with np.nan
    df = df.replace([np.inf, -np.inf], np.nan)
    # Drop any rows that contain NaN
    df = df.dropna(how='any')
    # Reset index and return a list of records
    return df.reset_index().to_dict(orient='records')

# Route for ticker basic info
@app.route('/stock/<ticker>', methods=['GET'])
def get_ticker_info(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)
        return jsonify(ticker_obj.info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stock/<ticker>/growth_estimates', methods=['GET'])
def get_growth_estimates(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)
        growth = ticker_obj.growth_estimates
        if growth is None or growth.empty:
            return jsonify({"error": "No growth estimates available"}), 404
        return jsonify(clean_json(growth)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stock/<ticker>/earnings', methods=['GET'])
def get_earnings(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)
        earnings = ticker_obj.earnings
        if earnings is None or earnings.empty:
            return jsonify({"error": "No earnings data available"}), 404
        return jsonify(clean_json(earnings)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stock/<ticker>/financials', methods=['GET'])
def get_financials(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)
        financials = ticker_obj.financials
        if financials is None or financials.empty:
            return jsonify({"error": "No financials data available"}), 404
        return jsonify(clean_json(financials)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stock/<ticker>/balance_sheet', methods=['GET'])
def get_balance_sheet(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)
        balance_sheet = ticker_obj.balance_sheet
        if balance_sheet is None or balance_sheet.empty:
            return jsonify({"error": "No balance sheet data available"}), 404
        return jsonify(clean_json(balance_sheet)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stock/<ticker>/cashflow', methods=['GET'])
def get_cashflow(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)
        cashflow = ticker_obj.cashflow
        if cashflow is None or cashflow.empty:
            return jsonify({"error": "No cashflow data available"}), 404
        return jsonify(clean_json(cashflow)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stock/<ticker>/sustainability', methods=['GET'])
def get_sustainability(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)
        sustainability = ticker_obj.sustainability
        if sustainability is None or sustainability.empty:
            return jsonify({"error": "No sustainability data available"}), 404
        return jsonify(clean_json(sustainability)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stock/<ticker>/recommendations', methods=['GET'])
def get_recommendations(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)
        recommendations = ticker_obj.recommendations
        if recommendations is None or recommendations.empty:
            return jsonify({"error": "No recommendations available"}), 404
        return jsonify(clean_json(recommendations)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stocks/close_prices', methods=['POST'])
def get_close_prices():
    try:
        data = request.get_json()
        tickers = data.get("tickers", [])
        if not tickers or not isinstance(tickers, list):
            return jsonify({"error": "Invalid or missing tickers list"}), 400

        end_date = datetime.today()
        start_date = end_date - timedelta(days=365)

        df = yf.download(tickers, start=start_date, end=end_date)["Close"]
        if df.empty:
            return jsonify({"error": "No data available for the given tickers"}), 404

        # Convert to structured format
        response = {
            "dates": df.index.strftime('%Y-%m-%d').tolist(),
            "prices": {ticker: df[ticker].tolist() for ticker in tickers}
        }

        return jsonify(clean_json(response)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stocks/close_prices_range', methods=['GET'])
def get_close_prices_range():
    try:
        tickers = request.args.getlist("ticker")
        start_date = request.args.get("start")
        end_date = request.args.get("end")

        # Validate input
        if not tickers:
            return jsonify({"error": "Missing tickers"}), 400
        if not start_date or not end_date:
            return jsonify({"error": "Missing start or end date"}), 400

        # Parse dates
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        df = yf.download(tickers, start=start, end=end, auto_adjust=False)["Close"]
        if df.empty:
            return jsonify({"error": "No data available for the given parameters"}), 404

        # Ensure all tickers are in the DataFrame (even if missing)
        for ticker in tickers:
            if ticker not in df.columns:
                df[ticker] = float('nan')

        response = {
            "dates": df.index.strftime('%Y-%m-%d').tolist(),
            "prices": {ticker: [None if pd.isna(v) else v for v in df[ticker].tolist()] for ticker in tickers}
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
