from flask import Flask, render_template, request
import hashlib
import math
import secrets
import string

app = Flask(__name__)

def analyze_password(password):
    length = len(password)

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    charset = 0
    if has_lower: charset += 26
    if has_upper: charset += 26
    if has_digit: charset += 10
    if has_special: charset += 32
    if charset == 0: charset = 1

    entropy = length * math.log2(charset)
    score = min(int((entropy / 80) * 100), 100)

    if score < 40:
        strength = "Weak"
        color = "#ff4d4d"
    elif score < 70:
        strength = "Moderate"
        color = "#ffb84d"
    else:
        strength = "Strong"
        color = "#4dff88"

    guesses_per_sec = 1_000_000_000
    crack_time = (2 ** entropy) / guesses_per_sec

    if crack_time < 60:
        crack_display = f"{round(crack_time,2)} seconds"
    elif crack_time < 3600:
        crack_display = f"{round(crack_time/60,2)} minutes"
    elif crack_time < 86400:
        crack_display = f"{round(crack_time/3600,2)} hours"
    else:
        crack_display = f"{round(crack_time/86400,2)} days"

    sha256_hash = hashlib.sha256(password.encode()).hexdigest()

    suggestions = []
    if length < 8: suggestions.append("Use at least 8 characters.")
    if not has_digit: suggestions.append("Include numbers.")
    if not has_special: suggestions.append("Include special characters.")
    if not has_upper: suggestions.append("Include uppercase letters.")

    strong_password = ''.join(secrets.choice(
        string.ascii_letters + string.digits + string.punctuation
    ) for _ in range(12))

    return {
        "score": score,
        "strength": strength,
        "color": color,
        "entropy": round(entropy, 2),
        "crack_time": crack_display,
        "hash": sha256_hash,
        "suggestions": suggestions,
        "strong_password": strong_password
    }

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        password = request.form.get("password")
        result = analyze_password(password)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
