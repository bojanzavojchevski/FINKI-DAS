from flask import Flask, request, jsonify
import mysql.connector
import pandas as pd
import ta


app = Flask(__name__)

# Database connection setup
def get_db_connection():
    return mysql.connect(
        host="localhost",
        user="root",
        password="lajnagomna123",  # Ensure this is correct
        database="stock_data",
    )

@app.route('/stockdata', methods=['POST'])
def get_stock_data():
    issuer_code = request.json.get('issuer_code')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch stock data for the selected issuer_code
    cursor.execute("SELECT * FROM stock_data WHERE issuer_code = %s", (issuer_code,))
    stock_data = cursor.fetchall()

    # Convert data to pandas DataFrame for analysis
    df = pd.DataFrame(stock_data)
    
    # Perform technical analysis (example with SMA)
    df['SMA_20'] = ta.trend.sma_indicator(df['avg_price'], window=20)
    df['EMA_20'] = ta.trend.ema_indicator(df['avg_price'], window=20)
    df['RSI'] = ta.momentum.rsi(df['avg_price'], window=14)
    df['MACD'] = ta.trend.macd(df['avg_price'])

    # Return the result as JSON
    result = df.to_dict(orient='records')
    
    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
