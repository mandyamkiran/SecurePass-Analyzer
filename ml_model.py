import pandas as pd
import string
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# ---- Feature Extraction ----

def extract_features(password):
    return {
        "length": len(password),
        "lowercase": sum(c.islower() for c in password),
        "uppercase": sum(c.isupper() for c in password),
        "digits": sum(c.isdigit() for c in password),
        "special": sum(c in string.punctuation for c in password)
    }

# ---- Sample Training Data ----

passwords = [
    "123456", "password", "admin",
    "Kiran123", "Welcome@2024",
    "Strong@Pass99", "XyZ!7890#Secure"
]

labels = [
    0, 0, 0,   # Weak
    1, 1,      # Moderate
    2, 2       # Strong
]

# Create dataframe
data = pd.DataFrame([extract_features(p) for p in passwords])
data["label"] = labels

# Split features and labels
X = data.drop("label", axis=1)
y = data["label"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Check accuracy
accuracy = model.score(X_test, y_test)
print("Model Accuracy:", accuracy)

# Save model
joblib.dump(model, "password_model.pkl")