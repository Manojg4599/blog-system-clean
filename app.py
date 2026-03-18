from flask import Flask, render_template, request, redirect
import os
import psycopg2
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

DB_URL = os.getenv("DB_URL")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")


def db():
    return psycopg2.connect(DB_URL, sslmode="require")


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


def init_db():

    conn=db()
    cur=conn.cursor()

    cur.execute("""

    CREATE TABLE IF NOT EXISTS orders(

    id SERIAL PRIMARY KEY,
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
    cur.close()
    conn.close()


init_db()


def send_email(name,email,ctype):

    try:

        price=PRICING.get(ctype)

        body=f"""
Hello {name},

Thank you for submitting your {ctype} request.

Our editorial team is preparing your article.

Preview Access
25% of the article will be visible initially.

Content Plans

Single Article: {price[0]}

Professional Plan: {price[1]}

Growth Plan: {price[2]}

Best Regards
ContentForge Editorial Team
"""

        msg=MIMEText(body)

        msg["Subject"]="ContentForge Request Received"
        msg["From"]=EMAIL_USER
        msg["To"]=email

        s=smtplib.SMTP("smtp.gmail.com",587)
        s.starttls()
        s.login(EMAIL_USER,EMAIL_PASS)
        s.send_message(msg)
        s.quit()

    except Exception as e:
        print("EMAIL ERROR:",e)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit",methods=["POST"])
def submit():

    name=request.form.get("name")
    email=request.form.get("email")
    ctype=request.form.get("type")
    topic=request.form.get("topic")
    audience=request.form.get("audience")
    keywords=request.form.get("keywords")
    brand=request.form.get("brand")
    website=request.form.get("website")
    details=request.form.get("details")

    if not name or not email or not topic or not keywords:

        return "Required fields missing"


    conn=db()
    cur=conn.cursor()

    cur.execute("""

    INSERT INTO orders
    (name,email,content_type,topic,audience,keywords,brand,website,instructions)

    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)

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
    details

    )

    )

    conn.commit()

    cur.close()
    conn.close()

    send_email(name,email,ctype)

    return redirect("/")
