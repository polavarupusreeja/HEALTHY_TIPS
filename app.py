from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import csv
import os

app = Flask(__name__)
app.secret_key = "secret123"

# Dummy users
USERS = {"admin": "1234", "sreeja": "1234", "varshitha": "1234"}

# Load Health Tips CSV
def load_health_tips():
    csv_path = os.path.join(os.path.dirname(__file__), "new", "health_tips.csv")
    tips = []
    try:
        with open(csv_path, mode="r", encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            # Expecting a header named 'Tips'
            for row in reader:
                tip = (row.get("Tips") or "").strip()
                if tip:
                    tips.append(tip)
    except FileNotFoundError:
        tips = []  # File missing; keep empty list
    except Exception:
        pass      # Any parsing error; keep what was read so far
    return tips

HEALTH_TIPS = load_health_tips()

# Routes
@app.route("/")
def home():
    return render_template("index.html")   # index.html is your login page

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip().lower()
        password = (request.form.get("password") or "").strip()

        if username in USERS and USERS[username] == password:
            session["user"] = username
            flash("Successfully logged in", "success")
            return redirect(url_for("about"))   # ✅ Go to About page after login
        else:
            flash("Invalid username or password", "error")
            return render_template("index.html")  # ✅ Back to login page if wrong

    return render_template("index.html")  # ✅ GET request shows login page

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/details")
def details():
    return render_template("details.html", tips=HEALTH_TIPS)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/api/tips", methods=["GET"])
def api_tips():
    return jsonify({"tips": HEALTH_TIPS})

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have logged out!", "success")
    return redirect(url_for("home"))   # back to login page

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Username and password are required", "error")
            return render_template("signup.html")

        if username in USERS:
            flash("User already exists", "error")
            return render_template("signup.html")

        USERS[username] = password
        session["user"] = username
        flash("Account created successfully", "success")
        return redirect(url_for("about"))

    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)
