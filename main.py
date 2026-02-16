import math
import hashlib
import string
import random

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

def brute_force_time(length, charset):
    attempts_per_sec = 1_000_000_000
    combinations = charset ** length
    seconds = combinations / attempts_per_sec
    return seconds

def format_time(seconds):
    years = seconds / (60*60*24*365)
    if years > 1:
        return f"{round(years,2)} years"
    elif seconds > 60:
        return f"{round(seconds/60,2)} minutes"
    else:
        return f"{round(seconds,2)} seconds"

def check_patterns(password):
    if password in common_passwords:
        return "Password found in common password list!"
    if password.isdigit() and password in "1234567890":
        return "Sequential number pattern detected!"
    if len(set(password)) == 1:
        return "Repeated character pattern detected!"
    return None

def generate_strong_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---- MAIN ----

password = input("Enter your password: ")

entropy, charset = calculate_entropy(password)
time_seconds = brute_force_time(len(password), charset)
formatted_time = format_time(time_seconds)
pattern_warning = check_patterns(password)
hashed = hash_password(password)

print("\n--- Advanced Password Analysis ---")
print("Entropy:", round(entropy,2), "bits")
print("Estimated Crack Time:", formatted_time)
print("SHA-256 Hash:", hashed)

if pattern_warning:
    print("⚠ Warning:", pattern_warning)

if entropy < 50:
    print("🔐 Suggested Strong Password:", generate_strong_password())
