from flask import Flask, render_template, request, redirect
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Database file location
DATABASE = "database/database.db"

# Email credentials from Render environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    if not os.path.exists("database"):
        os.makedirs("database")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        content_type TEXT,
        topic TEXT,
        audience TEXT,
        keywords TEXT,
        brand TEXT,
        website TEXT,
        instructions TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


init_db()


PRICING = {

"Blog Article":("₹1050","₹8500 / month (10)","₹12000 / month (15)"),
"SEO Landing Page":("₹1250","₹10000 / month (10)","₹14000 / month (15)"),
"Comparison Article":("₹1150","₹9200 / month (10)","₹13000 / month (15)"),
"Educational Guide":("₹1350","₹10800 / month (10)","₹15000 / month (15)"),
"FAQ Page":("₹900","₹7200 / month (10)","₹10000 / month (15)"),
"Tool Page":("₹1200","₹9500 / month (10)","₹13500 / month (15)"),
"Directory Page":("₹1100","₹8800 / month (10)","₹12500 / month (15)"),
"Speech":("₹1500","₹12000 / month (10)","₹17000 / month (15)"),
"Essay":("₹900","₹7000 / month (10)","₹9500 / month (15)"),
"Official Letter":("₹700","₹5500 / month (10)","₹7500 / month (15)")
}


def send_email(name,email,ctype):

    try:

        price = PRICING.get(ctype)

        body = f"""
Hello {name},

Thank you for submitting your {ctype} request.

Our editorial team has received your request and will begin preparing your content package.

Preview Access
25% of the article will be available for preview.

Content Plans

Single Article: {price[0]}

Professional Plan: {price[1]}

Growth Plan: {price[2]}

Best Regards
ContentForge Editorial Team
"""

        msg = MIMEText(body)

        msg["Subject"] = "ContentForge Request Received"
        msg["From"] = EMAIL_USER
        msg["To"] = email

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(EMAIL_USER,EMAIL_PASS)
        server.send_message(msg)
        server.quit()

    except Exception as e:
        print("EMAIL ERROR:",e)


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
    keywords = request.form.get("keywords")
    brand = request.form.get("brand")
    website = request.form.get("website")
    instructions = request.form.get("details")

    if not name or not email or not topic or not keywords:
        return "Required fields missing"

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO orders
    (name,email,content_type,topic,audience,keywords,brand,website,instructions)
    VALUES(?,?,?,?,?,?,?,?,?)
    """,
    (
    name,
    email,
    ctype,
    topic,
    audience,
    keywords,
    brand,
    website,
    instructions
    )
    )

    conn.commit()
    conn.close()

    send_email(name,email,ctype)

    return redirect("/success")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/dashboard")
def dashboard():

    conn = get_db()

    orders = conn.execute(
        "SELECT * FROM orders ORDER BY created_at DESC"
    ).fetchall()

    conn.close()

    return render_template("dashboard.html",orders=orders)


if __name__ == "__main__":
    app.run()
