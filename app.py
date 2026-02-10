from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
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

# ---------------- FLASK-LOGIN SETUP ----------------
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(id=user[0], email=user[1], password=user[2])
    return None

# Context processor to make current_user available in templates
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

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
            user_id = cursor.lastrowid
            conn.close()

            # Log in the user immediately after signup
            user = User(id=user_id, email=email, password=password)
            login_user(user)
            return redirect(url_for("dashboard"))

        except sqlite3.IntegrityError:
            conn.close()
            return "❌ Email already exists!"

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            user_obj = User(id=user[0], email=user[1], password=user[2])
            login_user(user_obj)
            return redirect(url_for("dashboard"))
        else:
            return "❌ Invalid credentials!"

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return f"Welcome, {current_user.email}! <br> <a href='/logout'>Logout</a>"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ---------------- MAIN ----------------
if __name__ == "__main__":
    init_db()   # Creates the database if it doesn't exist
    app.run(debug=True)
