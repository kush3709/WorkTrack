from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///database.db")

@app.route("WorkTrack/", methods=["GET", "POST"])
def index():
    if not session.get("username"):
        return redirect("/login", code=307)
    return render_template("index.html", username=session["username"])

@app.route("/WorkTrack/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and request.form.get("username") != None and request.form.get("password") != None:
        entered_username = request.form.get("username")
        entered_password = request.form.get("password")
        user_data = db.execute("SELECT * FROM credentials WHERE username = ?", entered_username)
        if user_data:
            if user_data[0]["password"] == entered_password:
                session["username"] = entered_username
                return redirect("/")
            else:
                return render_template("login.html", error="Invalid password")
        else:
            return render_template("login.html", error="Invalid username")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST" and request.form.get("username") != None and request.form.get("password") != None:
        entered_username = request.form.get("username")
        entered_password = request.form.get("password")
        user_data = db.execute("SELECT * FROM credentials WHERE username = ?", entered_username)
        if user_data:
            return render_template("signup.html", error="Username in use")
        else:
            db.execute("INSERT INTO credentials (username, password) VALUES (?, ?)", entered_username, entered_password)
            session["username"] = entered_username
            return redirect("/")
    return render_template("signup.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session["username"] = None
    return redirect("/")

@app.route("/goals", methods=["GET", "POST"])
def goals():
    if not session.get("username"):
        return redirect("/")
    goal_results = db.execute("SELECT goal FROM goals WHERE username = ?", session["username"])
    user_goals = [result["goal"] for result in goal_results]
    return render_template("goals.html", goals=user_goals)

@app.route("/delete_goal", methods=["POST"])
def delete_goal():
    data = request.get_json()
    goal = data.get("goal")
    db.execute("DELETE FROM goals WHERE username = ? AND goal = ?", session["username"], goal)
    return redirect("/goals")

@app.route("/log", methods=["GET", "POST"])
def log():
    if not session.get("username"):
        return redirect("/")
    log_results = db.execute("SELECT * FROM logs WHERE username = ?", session["username"])
    return render_template("log.html", logs=log_results)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.form.get('goal') is not None:
        new_goal = request.form.get('goal')
        db.execute("INSERT INTO goals (username, goal) VALUES (?, ?)", session["username"], new_goal)
        return redirect("/goals")
    elif request.form.get('type') is not None:
        type = request.form.get('type')
        duration = request.form.get('duration')
        worked = request.form.get('worked')
        date = request.form.get('date')
        db.execute("INSERT INTO logs (username, type, duration, worked, date) VALUES (?, ?, ?, ?, ?)", session["username"], type, duration, worked, date)
        return redirect("/log")

@app.route("/account", methods=["GET", "POST"])
def account():
    if not session.get("username"):
        return redirect("/")
    if request.method == "POST":
        old = db.execute("SELECT * FROM credentials WHERE username = ? AND password = ?", session["username"], request.form.get("current"))
        if old:
            if request.form.get("new") == request.form.get("newbackup"):
                db.execute("UPDATE credentials SET password = ? WHERE username = ?", request.form.get("new"), session["username"])
                return render_template("account.html", message="Success!")
            else:
                render_template("account.html", message="New passwords do not match, try again.")
        else:
            return render_template("account.html", message="Old password does not exist, try again.")
    return render_template("account.html")

@app.route("/sessions", methods=["GET", "POST"])
def sessions():
    if not session.get("username"):
        return redirect("/")
    return render_template("sessions.html")

@app.route("/sessions/push", methods=["GET", "POST"])
def push():
    return render_template("sessions/push.html")

@app.route("/sessions/pull", methods=["GET", "POST"])
def pull():
    return render_template("sessions/pull.html")

@app.route("/sessions/legs", methods=["GET", "POST"])
def legs():
    return render_template("sessions/legs.html")

@app.route("/sessions/core", methods=["GET", "POST"])
def core():
    return render_template("sessions/core.html")

@app.route("/sessions/plyos", methods=["GET", "POST"])
def plyos():
    return render_template("sessions/plyos.html")

@app.route("/sessions/speed", methods=["GET", "POST"])
def speed():
    return render_template("sessions/speed.html")

@app.route("/sessions/acceleration", methods=["GET", "POST"])
def accel():
    return render_template("sessions/acceleration.html")

@app.route("/sessions/cardio", methods=["GET", "POST"])
def cadio():
    return render_template("sessions/cardio.html")

@app.route("/sessions/flexibility", methods=["GET", "POST"])
def flexiblity():
    return render_template("sessions/flexibility.html")

@app.route("/sessions/warmup", methods=["GET", "POST"])
def warmup():
    return render_template("sessions/warmup.html")

@app.route("/sessions/cooldown", methods=["GET", "POST"])
def cooldown():
    return render_template("sessions/cooldown.html")

@app.route("/sessions/stretching", methods=["GET", "POST"])
def stretching():
    return render_template("sessions/stretching.html")
