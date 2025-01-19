from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Get the database connection from environment variables (or default to local values)
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),  # Use environment variable for host
        user=os.getenv("DB_USER", "root"),  # Use environment variable for user
        password=os.getenv("DB_PASSWORD", "lajnagomna123"),  # Use environment variable for password
        database=os.getenv("DB_NAME", "stock_data")  # Use environment variable for database name
    )

@app.route('/issuers', methods=['GET'])
def get_issuers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT issuer_code FROM stock_data")
        issuers = [row["issuer_code"] for row in cursor.fetchall()]
        conn.close()

        return jsonify(issuers)
    except mysql.connector.Error as e:
        app.logger.error(f"Database error: {str(e)}")
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
