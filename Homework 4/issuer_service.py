from flask import Flask, jsonify
import mysql.connector


app = Flask(__name__)

# Database connection setup
def get_db_connection():
    return mysql.connect(
        host="localhost",
        user="root",
        password="lajnagomna123",  # Ensure this is correct
        database="stock_data",
        
    )

@app.route('/issuers', methods=['GET'])
def get_issuers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT issuer_code FROM stock_data")
    issuers = [row["issuer_code"] for row in cursor.fetchall()]
    conn.close()

    return jsonify(issuers)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
