from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

DB_NAME = "users.db"

# ---------------- DATABASE INIT ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return redirect(url_for("signup"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, password)
            )
            conn.commit()
            conn.close()
            return "✅ Signup Successful!"
        except sqlite3.IntegrityError:
            conn.close()
            return "❌ Email already exists!"

    return render_template("signup.html")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    init_db()   # 👈 THIS CREATES users.db
    app.run(host="0.0.0.0", port=10000)
