from flask import Flask, render_template, request, jsonify
import joblib
from datetime import datetime
import json
import os
import random

app = Flask(__name__)

# ---------------- LOAD MODEL ----------------
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# ---------------- HISTORY ----------------
HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

history = load_history()

# ---------------- LOCAL AI (ML MODEL) ----------------
def local_predict(msg):
    data = vectorizer.transform([msg])

    pred = model.predict(data)[0]
    probs = model.predict_proba(data)[0]

    confidence = float(max(probs) * 100)

    result = "SCAM" if int(pred) == 1 else "LEGITIMATE"

    return result, round(confidence, 2)

# ---------------- CLOUD AI (DIFFERENT LOGIC) ----------------
@app.route("/cloud-api", methods=["POST"])
def cloud_api():

    msg = request.json.get("message", "").lower()

    # Rule-based cloud system (different from ML)
    scam_keywords = ["win", "lottery", "prize", "urgent", "free", "click", "blocked", "verify"]

    if any(word in msg for word in scam_keywords):
        result = "SCAM"
        confidence = random.uniform(85, 95)
    else:
        result = "LEGITIMATE"
        confidence = random.uniform(70, 85)

    return jsonify({
        "result": result,
        "confidence": round(confidence, 2)
    })

# ---------------- CLOUD CALL FROM FLASK ----------------
def cloud_predict(msg):
    try:
        import requests

        url = "http://127.0.0.1:5000/cloud-api"

        response = requests.post(url, json={"message": msg}, timeout=5)
        data = response.json()

        return data["result"], float(data["confidence"])

    except Exception as e:
        print("Cloud error:", e)
        return "CLOUD ERROR", 0.0

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- PREDICT ----------------
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json(force=True)

    msg = data.get("message", "")
    mode = data.get("mode", "LOCAL AI")

    local_result, local_conf = local_predict(msg)
    cloud_result, cloud_conf = cloud_predict(msg)

    if mode == "LOCAL AI":
        result = local_result
        confidence = local_conf
    else:
        result = cloud_result
        confidence = cloud_conf

    # ---------------- SAVE HISTORY ----------------
    history.append({
        "message": msg,
        "result": result,
        "confidence": confidence,
        "mode": mode,
        "time": datetime.now().strftime("%H:%M:%S")
    })

    save_history(history)

    return jsonify({
        "result": result,
        "confidence": confidence,
        "mode": mode,
        "history": history,
        "local_result": local_result,
        "cloud_result": cloud_result
    })

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)