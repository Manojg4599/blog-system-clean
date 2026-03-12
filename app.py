from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    data = request.json

    print("New Request:", data)

    return jsonify({
        "status":"success",
        "message":"Your request has been submitted!"
    })


@app.route("/dashboard")
def dashboard():
    return "ContentForge Admin Dashboard"


if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)
