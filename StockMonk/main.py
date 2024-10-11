from flask import Flask, request, jsonify
import yfinance as yf
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
cors = CORS(app, 
    resources={r"/api/*": {"origins": ["http://127.0.0.1:8000"]}},
    hods=["POST"],
    allow_headers=["Content-Type"],
    supports_credentials=True
)

@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self';"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Permissions-Policy'] = "geolocation=(), microphone=(), camera=()"
    return response

@app.route('/api/get-stock-data', methods=['POST'])
def get_stock_data():
    try:
        data = request.get_json()
        ticker_id = data.get('ticker_id')
        stock = yf.Ticker(ticker_id)
        start = datetime(2024, 8, 15)
        end = datetime(2024, 9, 15)
        try:
            history = stock.history(start=start, end=end)
        except Exception as e:
            print(e)
        response_data = {
            'x': history.index.strftime('%Y-%m-%d').tolist(),
            'open': history['Open'].tolist(),
            'high': history['High'].tolist(),
            'low': history['Low'].tolist(),
            'close': history['Close'].tolist(),
            'ticker_id': ticker_id
        }
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
