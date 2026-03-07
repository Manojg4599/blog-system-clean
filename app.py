from flask import Flask, request, jsonify, render_template
from db import get_db_connection, create_tables

app = Flask(__name__)

create_tables()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/demo-request", methods=["POST"])
def demo_request():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    industry = data.get("industry")
    blog_topic = data.get("blog_topic")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO demo_requests (name,email,industry,blog_topic)
        VALUES (%s,%s,%s,%s)
        """,
        (name, email, industry, blog_topic)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Request saved"})


if __name__ == "__main__":
    app.run()
