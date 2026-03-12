from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Home Page
@app.route("/")
def home():
    return "ContentForge Blog System Running Successfully!"

# Demo order endpoint
@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    return jsonify({
        "status": "success",
        "message": "Order received",
        "data": data
    })

# Dashboard
@app.route("/dashboard")
def dashboard():
    return "ContentForge Dashboard"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
