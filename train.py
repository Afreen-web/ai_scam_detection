import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# ---------------- LOAD DATA ----------------
df = pd.read_csv("dataset.csv", encoding="utf-8", on_bad_lines="skip")

print("Original data shape:", df.shape)

# ---------------- CLEAN ----------------
df = df.dropna(subset=["message", "label"])

# FORCE numeric labels
df["label"] = df["label"].astype(int)

# ---------------- CHECK BALANCE ----------------
print("\nClass distribution:")
print(df["label"].value_counts())

# ---------------- FEATURES ----------------
X = df["message"]
y = df["label"]

# ---------------- SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y   # 🔥 IMPORTANT FIX
)

# ---------------- VECTORIZE ----------------
vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words="english")

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ---------------- MODEL ----------------
model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced"
)

model.fit(X_train_vec, y_train)

# ---------------- EVALUATION ----------------
y_pred = model.predict(X_test_vec)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# ---------------- SAVE MODEL ----------------
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("\n✅ Model trained successfully!")