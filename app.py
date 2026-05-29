import os
from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from database import init_db
from authenticate import authenticate_user

# ВИПРАВЛЕНО: Імпортуємо саме evaluate_access
from policies import evaluate_access
from logging_utils import log_event

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        device = request.form.get("device")
        network = request.form.get("network")

        # Автентифікація через SQLite
        user = authenticate_user(username, password)

        if user:
            # ВИПРАВЛЕНО: Викликаємо правильну функцію evaluate_access
            decision, score, reason = evaluate_access(user["role"], device, network)

            # Передаємо всі 7 параметрів у логер подій безпеки
            log_event(username, user["role"], device, network, decision, score, reason)

            if decision in ["ALLOW", "LIMITED"]:
                session["user"] = user["username"]
                session["role"] = user["role"]
                session["access_level"] = decision
                session["trust_score"] = score
                return redirect(url_for("dashboard"))
            else:
                # Якщо рушій повернув DENY
                return render_template("denied.html", reason=reason, score=score)
        else:
            # Невірний логін або пароль
            log_event(
                username, "UNKNOWN", device, network, "DENY", 0, "Invalid credentials"
            )
            return render_template(
                "login.html", error="Невірне ім'я користувача або пароль."
            )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    # Захист від прямого переходу без сесії
    if "user" not in session:
        return redirect(url_for("login"))

    user_data = {"username": session["user"], "role": session["role"]}

    return render_template(
        "dashboard.html",
        user=user_data,
        access_level=session["access_level"],
        score=session["trust_score"],
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    print("[INIT] Створення конфігураційних файлів логів...")
    print("[INIT] Иніціалізація бази даних SQLite...")
    init_db()

    print("[SYSTEM] Запуск Zero Trust веб-сервера...")
    app.run(debug=True, port=5000)
