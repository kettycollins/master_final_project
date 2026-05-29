import os
from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from database import init_db
from authenticate import authenticate_user
from policies import evaluate_access
from logging_utils import log_event

app = Flask(__name__)
app.jinja_env.filters["uppercase"] = lambda s: s.upper() if s else ""
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
            # Обчислення рішення Zero Trust
            decision, score, reason = evaluate_access(user["role"], device, network)

            # Логування події
            log_event(username, user["role"], device, network, decision, score, reason)

            # Записуємо дані в сесію для використання в шаблонах
            session["user"] = user["username"]
            session["role"] = user["role"]
            session["access_level"] = decision
            session["trust_score"] = score
            session["reason"] = reason

            # Передаємо рішення прямо в шаблон для зміни кольору (Зелений / Жовтий / Червоний)
            return render_template(
                "denied.html", decision=decision, score=score, reason=reason
            )
        else:
            log_event(
                username, "UNKNOWN", device, network, "DENY", 0, "Invalid credentials"
            )
            return render_template(
                "login.html", error="Невірне ім'я користувача або пароль."
            )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    # 1. Захист від прямого переходу (Перевіряємо, чи користувач взагалі автентифікований)
    if "user" not in session:
        return redirect(url_for("login"))

    # 2. Якщо вердикт DENY або взагалі відсутній — повна заборона, повертаємо на вхід
    if session.get("access_level") not in ["ALLOW", "LIMITED"]:
        return redirect(url_for("login"))

    # Збираємо актуальні дані з сесії
    user_role = session.get("role")
    access_level = session.get("access_level")
    score = session.get("trust_score")

    user_data = {"username": session["user"], "role": user_role}

    # 3. ГІЛКА АДМІНІСТРАТОРА (Доступно тільки ролі admin І тільки з повним довіреним контекстом ALLOW)
    if user_role == "admin" and access_level == "ALLOW":
        # У майбутньому тут можна зчитувати JSON-логи безпеки для відображення
        return render_template("admin_dashboard.html", user=user_data, score=score)

    # 4. ГІЛКА КОРИСТУВАЧІВ (Вчителі та учні, які отримали ALLOW або LIMITED)
    elif user_role in ["teacher", "student"]:
        return render_template(
            "resource_page.html", user=user_data, access_level=access_level, score=score
        )

    # Безпечний фолбек: якщо роль невідома, очищуємо сесію та повертаємо на вхід
    return redirect(url_for("login"))


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
