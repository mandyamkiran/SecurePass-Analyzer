from flask import Flask, render_template, request
import math
import string
import hashlib
import random
import os

app = Flask(__name__)

# -----------------------------
# Common Weak Password List
# -----------------------------
COMMON_PASSWORDS = [
    "123456", "password", "12345678", "qwerty",
    "abc123", "admin", "123456789", "welcome",
    "password123", "12345"
]

# -----------------------------
# Entropy Calculation
# -----------------------------
def calculate_entropy(password):
    charset = 0

    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(c in string.punctuation for c in password):
        charset += 32

    entropy = len(password) * math.log2(charset) if charset else 0
    return entropy, charset

# -----------------------------
# Crack Time Formatter
# -----------------------------
def format_time(seconds):
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    years = days / 365

    if years >= 1:
        return f"{round(years, 2)} years"
    elif days >= 1:
        return f"{round(days, 2)} days"
    elif hours >= 1:
        return f"{round(hours, 2)} hours"
    elif minutes >= 1:
        return f"{round(minutes, 2)} minutes"
    else:
        return f"{round(seconds, 2)} seconds"

# -----------------------------
# Strong Password Generator
# -----------------------------
def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# -----------------------------
# Security Score Calculator
# -----------------------------
def calculate_score(password, entropy):
    score = 0

    if len(password) >= 12:
        score += 25
    elif len(password) >= 8:
        score += 15
    else:
        score += 5

    if any(c.islower() for c in password):
        score += 15
    if any(c.isupper() for c in password):
        score += 15
    if any(c.isdigit() for c in password):
        score += 15
    if any(c in string.punctuation for c in password):
        score += 15

    if entropy >= 60:
        score += 15
    elif entropy >= 40:
        score += 10
    else:
        score += 5

    return min(score, 100)

# -----------------------------
# Main Route
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        password = request.form.get("password")

        if password:
            entropy, charset = calculate_entropy(password)
            crack_time_seconds = (charset ** len(password)) / 1_000_000_000 if charset else 0
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            score = calculate_score(password, entropy)

            # Strength label
