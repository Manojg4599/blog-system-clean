from flask import Flask, render_template
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Ensure records folders exist
os.makedirs("records/demo", exist_ok=True)
os.makedirs("records/paid", exist_ok=True)


@app.route("/")
def home():
    return render_template(
        "index.html",
        business_name=Config.BUSINESS_NAME
    )


@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        business_name=Config.BUSINESS_NAME
    )


if __name__ == "__main__":
    app.run(debug=True)
