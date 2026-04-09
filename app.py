from flask import Flask, render_template, request
from utils.predictor import predict_message
from database.queries import create_table, insert_scam, get_all_history

app = Flask(__name__)

# Initialize DB
create_table()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        message = request.form["message"]

        result, confidence = predict_message(message)

        if result == "scam":
            return render_template("scam.html", message=message, confidence=confidence)
        else:
            return render_template("legit.html", message=message, confidence=confidence)

    return render_template("index.html")


@app.route("/report", methods=["POST"])
def report():
    message = request.form["message"]
    insert_scam(message)
    return "Reported Successfully"


@app.route("/history")
def history():
    data = get_all_history()
    return render_template("history.html", data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
    