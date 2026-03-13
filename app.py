from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

DATA_FILE = "orders.json"


def save_request(data):

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

    with open(DATA_FILE, "r") as f:
        orders = json.load(f)

    orders.append(data)

    with open(DATA_FILE, "w") as f:
        json.dump(orders, f, indent=4)


def load_requests():

    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    data = request.json

    save_request(data)

    return jsonify({
        "status": "success",
        "message": "Your request has been successfully submitted."
    })


@app.route("/dashboard")
def dashboard():

    orders = load_requests()

    return render_template("dashboard.html", orders=orders)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
