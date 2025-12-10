from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "mysecretkey123"

# ---------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------
def create_tables():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )''')

    conn.commit()
    conn.close()

create_tables()

# ---------------------------------------
# ROUTES
# ---------------------------------------

# HOME → redirect to login
@app.route("/")
def home():
    return redirect("/login")


# LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", 
                  (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid login details")

    return render_template("login.html")


# SIGNUP PAGE
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (username, password) VALUES (?,?)",
                      (username, password))
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            conn.close()
            return render_template("signup.html", error="Username already exists")

    return render_template("signup.html")


# DASHBOARD PAGE
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", username=session["user"])


# TAKE EXAM PAGE
@app.route("/take_exam")
def take_exam():
    if "user" not in session:
        return redirect("/login")
    return render_template("exam.html")


# RESULTS PAGE
@app.route("/results")
def results():
    if "user" not in session:
        return redirect("/login")
    return render_template("results.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------------------------------
# RUN SERVER
# ---------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
