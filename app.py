from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import os
import pickle
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

# DB CONNECTION
db = sqlite3.connect('database.db', check_same_thread=False)
cursor = db.cursor()

# CREATE TABLES
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    review TEXT,
    sentiment TEXT,
    rating INTEGER
)
""")
db.commit()

# LOAD MODEL
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE username=?", (user,))
        result = cursor.fetchone()

        if result and check_password_hash(result[2], pwd):
            session["user"] = user
            return redirect("/dashboard")
        else:
            flash("Invalid username or password")

    return render_template("login.html")

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        hashed_pwd = generate_password_hash(pwd)

        try:
            # CHECK IF USER EXISTS
            cursor.execute("SELECT * FROM users WHERE username=?", (user,))
            existing = cursor.fetchone()

            if existing:
                return "Username already exists ❗"

            cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)", (user, hashed_pwd))
            db.commit()

            return redirect('/')

        except Exception as e:
            return str(e)

    return render_template('register.html')

# DASHBOARD
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        product = request.form['product']
        review = request.form['review'].lower().strip()
        rating = int(request.form['rating'])

        review_vector = vectorizer.transform([review])
        prediction = model.predict(review_vector)[0]

        cursor.execute(
            "INSERT INTO reviews(product, review, sentiment, rating) VALUES(?,?,?,?)",
            (product, review, prediction, rating)
        )
        db.commit()

    cursor.execute("SELECT * FROM reviews")
    reviews = cursor.fetchall()

    cursor.execute("SELECT sentiment, COUNT(*) FROM reviews GROUP BY sentiment")
    data = cursor.fetchall()

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    return render_template("dashboard.html", reviews=reviews, labels=labels, values=values)

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# RUN APP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))