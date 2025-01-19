from flask import Flask, request, jsonify
import mysql.connector
import pandas as pd
import ta
from mysql.connector import Error

app = Flask(__name__)

# Database connection setup
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="db",
            user="root",
            password="lajnagomna123", 
            database="stock_data",
        )
    except Error as e:
        return None

@app.route('/stockdata', methods=['POST'])
def get_stock_data():
    issuer_code = request.json.get('issuer_code')
    
    if not issuer_code:
        return jsonify({"error": "Issuer code is required"}), 400

    conn = get_db_connection()
    
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM stock_data WHERE issuer_code = %s", (issuer_code,))
        stock_data = cursor.fetchall()
        
        if not stock_data:
            return jsonify({"error": f"No stock data found for issuer code: {issuer_code}"}), 404
        
        # Convert data to pandas DataFrame for analysis
        df = pd.DataFrame(stock_data)
        
        # Perform technical analysis (example with SMA, EMA, RSI, MACD)
        df['SMA_20'] = ta.trend.sma_indicator(df['avg_price'], window=20)
        df['EMA_20'] = ta.trend.ema_indicator(df['avg_price'], window=20)
        df['RSI'] = ta.momentum.rsi(df['avg_price'], window=14)
        df['MACD'] = ta.trend.macd(df['avg_price'])

        # Return the result as JSON
        result = df.to_dict(orient='records')

    except Error as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    finally:
        conn.close()

    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
