from flask import Flask, render_template, request, jsonify
import os
import psycopg2

app = Flask(__name__)

# Database connection
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


# Ensure table exists when server starts
init_db()


@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# SUBMIT CONTENT REQUEST
# ==============================

@app.route("/submit", methods=["POST"])
def submit():

    data = request.get_json()

    required = ["type", "topic", "audience", "length"]

    for field in required:

        if not data.get(field):

            return jsonify({
                "status": "error",
                "message": f"The field '{field}' is required. Please complete it."
            })

    try:

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

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": "System error while saving request."
        })


# ==============================
# DASHBOARD
# ==============================

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


# ==============================
# KEYWORD GENERATOR ENGINE
# ==============================

@app.route("/keywords", methods=["POST"])
def keywords():

    data = request.get_json()

    topic = data.get("topic", "").lower()

    if not topic:
        return jsonify({"keywords": []})

    suggestions = [

        topic,
        f"best {topic}",
        f"{topic} guide",
        f"{topic} comparison",
        f"top {topic}",
        f"{topic} benefits",
        f"{topic} for beginners",
        f"how to choose {topic}",
        f"{topic} tools",
        f"{topic} vs alternatives"
    ]

    return jsonify({"keywords": suggestions})


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
