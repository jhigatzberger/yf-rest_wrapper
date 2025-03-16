from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/stock', methods=['GET'])
def get_stock_info():
    ticker = request.args.get('ticker')

    if not ticker:
        return jsonify({"error": "Ticker parameter is required"}), 400

    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return jsonify(info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
