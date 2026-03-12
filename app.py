from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import datetime

from config import Config
from db import get_db_connection
from database import init_db
from dashboard import dashboard_bp

app = Flask(**name**)
app.config.from_object(Config)

# register dashboard routes

app.register_blueprint(dashboard_bp)

# ensure folders exist

os.makedirs("orders", exist_ok=True)
os.makedirs("database", exist_ok=True)

# initialize database

init_db()

@app.route("/")
def home():
return render_template("index.html")

@app.route("/submit-order", methods=["POST"])
def submit_order():

```
data = request.form

name = data.get("name")
email = data.get("email")
content_type = data.get("content_type")
topic = data.get("topic")
audience = data.get("audience")
purpose = data.get("purpose")
tone = data.get("tone")
length = data.get("length")
keywords = data.get("keywords")
instructions = data.get("instructions")
tier = data.get("tier")

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute(
    """
    INSERT INTO content_orders
    (name,email,content_type,topic,audience,purpose,tone,length,keywords,instructions,tier,status,created_time)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """,
    (
        name,
        email,
        content_type,
        topic,
        audience,
        purpose,
        tone,
        length,
        keywords,
        instructions,
        tier,
        "new",
        datetime.now(),
    ),
)

order_id = cursor.lastrowid

conn.commit()
conn.close()

order_folder = f"orders/order_{order_id}"
os.makedirs(order_folder, exist_ok=True)

order_data = {
    "order_id": order_id,
    "name": name,
    "email": email,
    "content_type": content_type,
    "topic": topic,
    "audience": audience,
    "purpose": purpose,
    "tone": tone,
    "length": length,
    "keywords": keywords,
    "instructions": instructions,
    "tier": tier,
}

with open(f"{order_folder}/input.json", "w") as f:
    json.dump(order_data, f, indent=4)

return jsonify({"status": "success", "order_id": order_id})
```

@app.route("/health")
def health():
return "OK"
