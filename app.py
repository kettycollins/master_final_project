from flask import Flask, render_template, request, redirect, session
from authenticate import authenticate_user
from policies import evaluate_access
from logging_utils import log_event, create_log_file
from database import init_db

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

        # Автентифікація користувача
        user = authenticate_user(username, password)
        if not user:
            return render_template(
                "denied.html", reason="Невірне ім'я користувача або пароль"
            )

        # Оцінка контексту безпеки рушієм політик
        decision, trust_score, reason = evaluate_access(
            role=user["role"], device=device, network=network
        )

        # Запис розширеної інформації в логи (важливо для диплому!)
        log_event(username, user["role"], device, network, decision)

        # Перевірка вердикту системи
        if decision == "DENY":
            return render_template("denied.html", reason=reason, score=trust_score)

        # Зберігаємо дані в сесію для захисту роутів
        session["user"] = username
        session["role"] = user["role"]
        session["access_level"] = decision
        session["trust_score"] = trust_score

        return render_template(
            "dashboard.html", user=user, access_level=decision, score=trust_score
        )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    # Захист роуту (Broken Access Control Fix)
    if "user" not in session:
        return redirect("/login")

    user_data = {"username": session["user"], "role": session["role"]}
    return render_template(
        "dashboard.html",
        user=user_data,
        access_level=session.get("access_level"),
        score=session.get("trust_score"),
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ПРАВИЛЬНА ІНІЦІАЛІЗАЦІЯ: спочатку створюємо файли й бази, а потім запускаємо сервер
if __name__ == "__main__":
    print("[INIT] Створення конфігураційних файлів логів...")
    create_log_file()

    print("[INIT] Ініціалізація бази даних SQLite...")
    init_db()

    print("[SYSTEM] Запуск Zero Trust веб-сервера...")
    app.run(debug=True)
