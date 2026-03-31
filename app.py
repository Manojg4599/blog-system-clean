from flask import Flask, render_template, request, redirect
import os
import psycopg2
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

DATABASE_URL = os.getenv("DB_URL")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def get_db():

    conn = psycopg2.connect(DATABASE_URL)

    return conn


def init_db():

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""

    CREATE TABLE IF NOT EXISTS orders(

        id SERIAL PRIMARY KEY,
        name TEXT,
        email TEXT,
        content_type TEXT,
        topic TEXT,
        audience TEXT,
        word_length TEXT,
        keywords TEXT,
        brand TEXT,
        website TEXT,
        instructions TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()
    cur.close()
    conn.close()


init_db()


def generate_keywords(topic):

    base = topic.lower()

    keywords = [
        base,
        f"{base} guide",
        f"{base} tips",
        f"best {base}",
        f"{base} strategies",
        f"how to {base}",
        f"{base} examples"
    ]

    return ", ".join(keywords)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name")
    email = request.form.get("email")
    ctype = request.form.get("type")
    topic = request.form.get("topic")
    audience = request.form.get("audience")
    length = request.form.get("length")
    keywords = request.form.get("keywords")
    brand = request.form.get("brand")
    website = request.form.get("website")
    details = request.form.get("details")

    if not keywords:
        keywords = generate_keywords(topic)

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""

    INSERT INTO orders
    (name,email,content_type,topic,audience,word_length,keywords,brand,website,instructions)

    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

    """,(name,email,ctype,topic,audience,length,keywords,brand,website,details))

    conn.commit()

    cur.close()
    conn.close()

    return redirect("/success")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/dashboard")
def dashboard():

    conn = get_db()

    cur = conn.cursor()

    cur.execute("SELECT * FROM orders ORDER BY created_at DESC")

    rows = cur.fetchall()

    orders=[]

    for r in rows:

        orders.append({

        "id":r[0],
        "name":r[1],
        "email":r[2],
        "content_type":r[3],
        "topic":r[4],
        "audience":r[5],
        "length":r[6],
        "keywords":r[7],
        "brand":r[8]

        })

    cur.close()
    conn.close()

    return render_template("dashboard.html",orders=orders)


if __name__ == "__main__":
    app.run()
