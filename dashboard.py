from utils.prompt_engine import generate_prompt
from db import get_db_connection

@app.route("/generate-prompt/<int:order_id>")
def generate_order_prompt(order_id):

    conn = get_db_connection()

    order = conn.execute(
        "SELECT * FROM content_orders WHERE id=?",
        (order_id,)
    ).fetchone()

    prompt = generate_prompt(order)

    order_folder = f"orders/order_{order_id}"

    with open(f"{order_folder}/prompt.txt","w") as f:
        f.write(prompt)

    return prompt
