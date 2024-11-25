from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key for session management

# Load the dataset
books_df = pd.read_csv(r"C:\Users\PRASANNA K\Desktop\SE PROJECT\Project\book_recommendations_with_ratings.csv")

# Sample user data
users = {}

def recommend_books(genre, narrative, time):
    """Recommend books based on user input."""
    filtered_books = books_df[
        (books_df['genre'] == genre) &
        (books_df['narrative'] == narrative)
    ]

    if time == 'short':
        filtered_books = filtered_books[filtered_books['length'] == 'short']
    elif time == 'medium':
        filtered_books = filtered_books[filtered_books['length'].isin(['short', 'medium'])]

    return filtered_books.to_dict(orient='records')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and check_password_hash(users[username], password):
            session["user"] = username
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username in users:
            flash("Username already exists", "warning")
        else:
            users[username] = generate_password_hash(password)
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    recommendations = []
    if request.method == "POST":
        genre = request.form.get("genre")
        narrative = request.form.get("narrative")
        time = request.form.get("time")
        recommendations = recommend_books(genre, narrative, time)

    return render_template("index.html", recommendations=recommendations)

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
