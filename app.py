import os
import json
from datetime import datetime
from db import get_db_connection

ORDERS_FOLDER = "orders"

@app.route("/submit-order", methods=["POST"])
def submit_order():

    data = request.form

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO content_orders
    (name,email,content_type,topic,audience,purpose,tone,length,keywords,instructions,tier)
    VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data["name"],
        data["email"],
        data["content_type"],
        data["topic"],
        data["audience"],
        data["purpose"],
        data["tone"],
        data["length"],
        data["keywords"],
        data["instructions"],
        data["tier"]
    ))

    order_id = cursor.lastrowid

    conn.commit()
    conn.close()

    order_folder = f"{ORDERS_FOLDER}/order_{order_id}"

    os.makedirs(order_folder, exist_ok=True)

    with open(f"{order_folder}/input.json","w") as f:
        json.dump(dict(data), f, indent=4)

    return "Order submitted successfully"
