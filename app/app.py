from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from mysql.connector import Error
import time
import os

app = Flask(__name__)

def get_db_connection():
    retries = 10
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST", "db"),
                user=os.getenv("MYSQL_USER", "user"),
                password=os.getenv("MYSQL_PASSWORD", "password"),
                database=os.getenv("MYSQL_DATABASE", "flaskdb")
            )
            print("Connected to MySQL!")
            return conn
        except Error as e:
            print("Database not ready, retrying in 5 seconds...")
            retries -= 1
            time.sleep(5)
    raise Exception("Could not connect to the database after retries")

@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        text = request.form.get("text")
        if text:
            cursor.execute("INSERT INTO messages (text) VALUES (%s)", (text,))
            conn.commit()
        return redirect(url_for("home"))

    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()
    conn.close()
    return render_template("index.html", messages=messages)

@app.route("/db-check")  # added route for DB check in tests, other wise not needed
def db_check():
    try:
        conn = get_db_connection()
        conn.close()
        return "DB connection successful!"
    except Exception as e:
        return f"DB connection failed: {e}", 500
    
    
if __name__ == "__main__":
    # Initialize table if not exists
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INT AUTO_INCREMENT PRIMARY KEY, text TEXT)")
    conn.commit()
    conn.close()
    app.run(host="0.0.0.0", port=5000)
