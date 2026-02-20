import math
import hashlib
import string
import secrets

common_passwords = ["123456", "password", "admin", "qwerty", "abc123"]

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


def detect_patterns(password):
    if password.lower() in common_passwords:
        return "Common password detected!"
    if len(set(password)) == 1:
        return "Repeated character pattern detected!"
    return None


def brute_force_time(length, charset):
    attempts_per_sec = 1_000_000_000
    combinations = charset ** length
    seconds = combinations / attempts_per_sec
    return seconds


def format_time(seconds):
    if seconds < 60:
        return f"{round(seconds,2)} seconds"
    elif seconds < 3600:
        return f"{round(seconds/60,2)} minutes"
    elif seconds < 86400:
        return f"{round(seconds/3600,2)} hours"
    else:
        return f"{round(seconds/86400,2)} days"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_strong_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))