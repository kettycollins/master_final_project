from flask import Flask, render_template, request, redirect, session
from authenticate import authenticate_user
from policies import evaluate_access
from logging_utils import log_event

app = Flask(__name__)
app.secret_key = "supersecretkey"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        device = request.form["device"]
        network = request.form["network"]

        user = authenticate_user(username, password)

        if not user:
            return render_template("denied.html", reason="Invalid credentials")

        decision = evaluate_access(role=user["role"], device=device, network=network)

        log_event(username, user["role"], device, network, decision)

        if decision == "ALLOW":
            session["user"] = username
            session["role"] = user["role"]
            return render_template("dashboard.html", user=user)

        return render_template("denied.html", reason="Access denied by policy")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

    # Create the database if it doesn't exist
    from database import create_database

    create_database()

    # Create the log file if it doesn't exist
    from logging_utils import create_log_file

    create_log_file()

    # Create the users table if it doesn't exist
    from database import create_users_table

    create_users_table()

    # Create the logs table if it doesn't exist
    from database import create_logs_table

    create_logs_table()

    # Create the policies table if it doesn't exist
    from database import create_policies_table

    create_policies_table()

    # Create the users table if it doesn't exist
    from database import create_users_table

    create_users_table()

    # Create the logs table if it doesn't exist
    from database import create_logs_table

    create_logs_table()

    # Create the policies table if it doesn't exist
    from database import create_policies_table

    create_policies_table()
