from flask import Flask, render_template, request, jsonify
import os
import psycopg2

app = Flask(__name__)

# Using new environment variable name
DB_URL = os.getenv("DB_URL")


def get_connection():
    return psycopg2.connect(DB_URL)


def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id SERIAL PRIMARY KEY,
        content_type TEXT,
        topic TEXT,
        audience TEXT,
        length TEXT,
        keywords TEXT,
        brand TEXT,
        instructions TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    data = request.json

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO orders
        (content_type, topic, audience, length, keywords, brand, instructions)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            data.get("type"),
            data.get("topic"),
            data.get("audience"),
            data.get("length"),
            data.get("keywords"),
            data.get("brand"),
            data.get("details")
        )
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Your request has been submitted successfully."
    })


@app.route("/dashboard")
def dashboard():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT content_type, topic, audience, length, keywords, brand
    FROM orders
    ORDER BY id DESC
    """)

    orders = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("dashboard.html", orders=orders)


if __name__ == "__main__":

    init_db()

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
