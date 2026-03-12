```python
from flask import Blueprint, render_template, request, redirect, url_for
import os

from db import get_db_connection
from utils.prompt_engine import generate_prompt

dashboard_bp = Blueprint("dashboard", __name__)

ORDERS_FOLDER = "orders"


# -----------------------------
# Dashboard Home
# -----------------------------
@dashboard_bp.route("/dashboard")
def dashboard_home():

    conn = get_db_connection()

    orders = conn.execute(
        "SELECT * FROM content_orders ORDER BY created_time DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        orders=orders
    )


# -----------------------------
# Generate Prompt
# -----------------------------
@dashboard_bp.route("/generate-prompt/<int:order_id>")
def generate_order_prompt(order_id):

    conn = get_db_connection()

    order = conn.execute(
        "SELECT * FROM content_orders WHERE id=?",
        (order_id,)
    ).fetchone()

    conn.close()

    if order is None:
        return "Order not found"

    prompt = generate_prompt(order)

    order_folder = os.path.join(ORDERS_FOLDER, f"order_{order_id}")

    os.makedirs(order_folder, exist_ok=True)

    prompt_file = os.path.join(order_folder, "prompt.txt")

    with open(prompt_file, "w") as f:
        f.write(prompt)

    return render_template(
        "prompt_view.html",
        prompt=prompt,
        order_id=order_id
    )


# -----------------------------
# Save AI Output
# -----------------------------
@dashboard_bp.route("/save-output/<int:order_id>", methods=["POST"])
def save_output(order_id):

    ai_output = request.form.get("ai_output")

    order_folder = os.path.join(ORDERS_FOLDER, f"order_{order_id}")

    os.makedirs(order_folder, exist_ok=True)

    output_file = os.path.join(order_folder, "ai_output.txt")

    with open(output_file, "w") as f:
        f.write(ai_output)

    return redirect(url_for("dashboard.dashboard_home"))
```
