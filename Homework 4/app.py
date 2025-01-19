from flask import Flask, render_template, request
import mysql.connector
import locale
import pandas as pd
import ta  # Technical Analysis Library

app = Flask(__name__)

# Set the locale to Macedonian (Macedonia) to format numbers correctly
locale.setlocale(locale.LC_ALL, 'mk_MK.UTF-8')

# Define the function to format numbers
def format_macedonian_number(value):
    if value is not None:
        return locale.format_string('%.2f', value, grouping=True).replace(",", "X").replace(".", ",").replace("X", ".")
    return "0,00"

app.jinja_env.filters['macedonian_format'] = format_macedonian_number

# Singleton pattern for database connection
class DatabaseConnection:
    _instance = None

    @staticmethod
    def get_connection():
        if DatabaseConnection._instance is None:
            DatabaseConnection._instance = mysql.connector.connect(
                host="localhost",
                user="root",
                password="lajnagomna123",
                database="stock_data"
            )
        return DatabaseConnection._instance

# Strategy Pattern for Technical Analysis
class TechnicalAnalysisStrategy:
    def apply(self, df):
        raise NotImplementedError("Subclasses should implement this method")

class SMAStrategy(TechnicalAnalysisStrategy):
    def apply(self, df):
        df['SMA_20'] = ta.trend.sma_indicator(df['avg_price'], window=20)
        df['SMA_Signal'] = df['SMA_20'].apply(lambda x: 'Buy' if x > df['avg_price'].iloc[-1] else 'Sell')
        return df

class EMAStrategy(TechnicalAnalysisStrategy):
    def apply(self, df):
        df['EMA_20'] = ta.trend.ema_indicator(df['avg_price'], window=20)
        df['EMA_Signal'] = df['EMA_20'].apply(lambda x: 'Buy' if x > df['avg_price'].iloc[-1] else 'Sell')
        return df

class RSIStrategy(TechnicalAnalysisStrategy):
    def apply(self, df):
        df['RSI'] = ta.momentum.rsi(df['avg_price'], window=14)
        df['RSI_Signal'] = df['RSI'].apply(lambda x: 'Buy' if x < 30 else 'Sell' if x > 70 else 'Hold')
        return df

@app.route('/')
def index():
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch all issuer codes for the dropdown
    cursor.execute("SELECT DISTINCT issuer_code FROM stock_data")
    issuer_codes = [row["issuer_code"] for row in cursor.fetchall()]

    return render_template('index.html', issuer_codes=issuer_codes)

@app.route('/data', methods=['POST'])
def display_data():
    issuer_code = request.form['issuer_code']
    strategy_type = request.form['strategy']  # New input to choose strategy
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch the data for the selected issuer code
    cursor.execute("SELECT * FROM stock_data WHERE issuer_code = %s", (issuer_code,))
    stock_data = cursor.fetchall()

    # Convert data to pandas DataFrame for analysis
    df = pd.DataFrame(stock_data)

    # Apply selected strategy
    if strategy_type == 'SMA':
        strategy = SMAStrategy()
    elif strategy_type == 'EMA':
        strategy = EMAStrategy()
    elif strategy_type == 'RSI':
        strategy = RSIStrategy()
    else:
        strategy = SMAStrategy()  # Default strategy

    df = strategy.apply(df)

    # Fetch all issuer codes to repopulate the dropdown
    cursor.execute("SELECT DISTINCT issuer_code FROM stock_data")
    issuer_codes = cursor.fetchall()

    return render_template(
        'data_table.html',
        stock_data=df.to_dict(orient='records'),
        issuer_code=issuer_code,
        issuer_codes=[code['issuer_code'] for code in issuer_codes]
    )


if __name__ == '__main__':
    app.run(debug=True)
