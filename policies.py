def evaluate_access(role, device, network):

    # Admin has full access only from trusted device
    if role == "admin":
        if device == "managed":
            return "ALLOW"
        return "DENY"

    # Teachers allowed from most contexts
    if role == "teacher":
        if network in ["school", "home"]:
            return "ALLOW"

    # Students restricted on unmanaged devices
    if role == "student":
        if device == "unmanaged":
            return "DENY"
        return "ALLOW"

    # Guests always restricted
    if role == "guest":
        return "DENY"

    return "DENY"
