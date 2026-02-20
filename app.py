from flask import Flask, render_template, request
import string
import joblib

from analyzer import (
    calculate_entropy,
    detect_patterns,
    brute_force_time,
    format_time,
    hash_password,
    generate_strong_password
)

# Load ML model
model = joblib.load("password_model.pkl")

app = Flask(__name__)


# ---------------- ML Prediction ---------------- #

def ml_predict_strength(password):
    features = [[
        len(password),
        sum(c.islower() for c in password),
        sum(c.isupper() for c in password),
        sum(c.isdigit() for c in password),
        sum(c in string.punctuation for c in password)
    ]]

    prediction = model.predict(features)[0]

    if prediction == 0:
        return "Weak"
    elif prediction == 1:
        return "Moderate"
    else:
        return "Strong"


# ---------------- Main Analyzer ---------------- #

def analyze_password(password):
    entropy, charset = calculate_entropy(password)
    pattern_warning = detect_patterns(password)

    crack_seconds = brute_force_time(len(password), charset)
    crack_display = format_time(crack_seconds)

    hashed = hash_password(password)

    # Security Score (Entropy based for UI circle)
    score = min(int((entropy / 80) * 100), 100)

    # ML-based strength prediction
    ml_strength = ml_predict_strength(password)

    if ml_strength == "Weak":
        color = "#ff4d4d"
    elif ml_strength == "Moderate":
        color = "#ffb84d"
    else:
        color = "#4dff88"

    return {
        "score": score,
        "strength": ml_strength,
        "color": color,
        "entropy": round(entropy, 2),
        "crack_time": crack_display,
        "hash": hashed,
        "pattern_warning": pattern_warning,
        "strong_password": generate_strong_password()
    }


# ---------------- Flask Route ---------------- #

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        password = request.form.get("password")
        if password:
            result = analyze_password(password)
    return render_template("index.html", result=result)


# ---------------- Run App ---------------- #

if __name__ == "__main__":
    app.run(debug=True)