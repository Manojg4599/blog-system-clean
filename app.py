from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from datetime import datetime

from config import Config
from config.content_types import CONTENT_TYPES
from db import get_db_connection
from database import init_db

# --------------------------------
# Flask App Initialization
# --------------------------------

app = Flask(__name__)
app.config.from_object(Config)

# --------------------------------
# Ensure Required Folders Exist
# --------------------------------

ORDERS_FOLDER = "orders"
DATABASE_FOLDER = "database"

os.makedirs(ORDERS_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)

# --------------------------------
# Initialize Database
# --------------------------------

init_db()

# --------------------------------
# Home Page
# --------------------------------

@app.route("/")
def home():
    return render_template(
        "index.html",
        content_types=CONTENT_TYPES,
        business_name=Config.BUSINESS_NAME
    )

# --------------------------------
# Submit Content Order
# --------------------------------

@app.route("/submit-order", methods=["POST"])
def submit_order():

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

    cursor.execute("""
        INSERT INTO content_orders
        (name,email,content_type,topic,audience,purpose,tone,length,keywords,instructions,tier,status,created_time)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
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
        datetime.now()
    ))

    order_id = cursor.lastrowid

    conn.commit()
    conn.close()

    # --------------------------------
    # Create Order Folder
    # --------------------------------

    order_folder = os.path.join(ORDERS_FOLDER, f"order_{order_id}")
    os.makedirs(order_folder, exist_ok=True)

    # --------------------------------
    # Save Order Input
    # --------------------------------

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
        "created_time": str(datetime.now())
    }

    with open(os.path.join(order_folder, "input.json"), "w") as f:
        json.dump(order_data, f, indent=4)

    return jsonify({
        "status": "success",
        "message": "Order submitted successfully",
        "order_id": order_id
    })

# --------------------------------
# List Orders (Basic Admin View)
# --------------------------------

@app.route("/orders")
def list_orders():

    conn = get_db_connection()

    orders = conn.execute(
        "SELECT * FROM content_orders ORDER BY created_time DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        orders=orders
    )

# --------------------------------
# View Single Order
# --------------------------------

@app.route("/order/<int:order_id>")
def view_order(order_id):

    conn = get_db_connection()

    order = conn.execute(
        "SELECT * FROM content_orders WHERE id=?",
        (order_id,)
    ).fetchone()

    conn.close()

    if order is None:
        return "Order not found"

    return jsonify(dict(order))

# --------------------------------
# Health Check (Render Friendly)
# --------------------------------

@app.route("/health")
def health():
    return "OK"

# --------------------------------
# Run App
# --------------------------------

if __name__ == "__main__":
    app.run(debug=True)
