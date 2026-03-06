from config import Config from flask import Flask, render_template
import os
from datetime import datetime, timedelta
from config import Config
from database import init_db, get_today_count

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
init_db()

# Ensure required folders exist
def ensure_folders():
    os.makedirs("records/demo", exist_ok=True)
    os.makedirs("records/paid", exist_ok=True)
    os.makedirs("static/css", exist_ok=True)

ensure_folders()

@app.route("/")
def home():
    return render_template("base.html",
                           business_name=Config.BUSINESS_NAME)

@app.route("/health")
def health():
    return "System Running Securely"

if __name__ == "__main__":
    app.run(debug=True)
