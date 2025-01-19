from flask import Flask, render_template, request
import requests
import locale

app = Flask(__name__)

# Set the locale to Macedonian (Macedonia) to format numbers correctly
locale.setlocale(locale.LC_ALL, 'mk_MK.UTF-8')

# Define the function to format numbers
def format_macedonian_number(value):
    if value is not None:
        return locale.format_string('%.2f', value, grouping=True).replace(",", "X").replace(".", ",").replace("X", ".")
    return "0,00"

# Register the filter with Jinja
app.jinja_env.filters['macedonian_format'] = format_macedonian_number

ISSUER_SERVICE_URL = "http://issuer:5001/issuers"
STOCK_DATA_SERVICE_URL = "http://stockdata:5002/stockdata"

@app.route('/')
def index():
    # Get the issuer codes from Issuer Service
    response = requests.get(ISSUER_SERVICE_URL)
    issuer_codes = response.json()
    return render_template('index.html', issuer_codes=issuer_codes)

@app.route('/data', methods=['POST'])
def display_data():
    issuer_code = request.form['issuer_code']

    # Get the stock data from Stock Data Service
    response = requests.post(STOCK_DATA_SERVICE_URL, json={'issuer_code': issuer_code})
    stock_data = response.json()

    return render_template('data_table.html', stock_data=stock_data, issuer_code=issuer_code)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
