users = {
    "anna": {"password": "student123", "role": "student"},
    "teacher1": {"password": "teacher123", "role": "teacher"},
    "admin1": {"password": "admin123", "role": "admin"},
    "guest": {"password": "guest123", "role": "guest"},
}


def authenticate_user(username, password):
    user = users.get(username)

    if user and user["password"] == password:
        return {"username": username, "role": user["role"]}

    return None


def authenticate_admin(username, password):
    user = users.get(username)

    if user and user["password"] == password and user["role"] == "admin":
        return {"username": username, "role": user["role"]}

    return None


def authenticate_teacher(username, password):
    user = users.get(username)

    if user and user["password"] == password and user["role"] == "teacher":
        return {"username": username, "role": user["role"]}

    return None


def authenticate_student(username, password):
    user = users.get(username)

    if user and user["password"] == password and user["role"] == "student":
        return {"username": username, "role": user["role"]}

    return None


def authenticate_guest(username, password):
    user = users.get(username)

    if user and user["password"] == password and user["role"] == "guest":
        return {"username": username, "role": user["role"]}

    return None
