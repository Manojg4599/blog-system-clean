from flask import Flask, render_template, request, jsonify
import os
import psycopg2
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

DB_URL = os.getenv("DB_URL")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")


# -----------------------------
# DATABASE CONNECTION
# -----------------------------

def db():
    return psycopg2.connect(DB_URL, sslmode="require")


# -----------------------------
# PRICING TABLE
# -----------------------------

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


# -----------------------------
# CREATE DATABASE TABLE
# -----------------------------

def init_db():

    try:

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

    except Exception as e:
        print("DB INIT ERROR:",e)


init_db()


# -----------------------------
# CLIENT EMAIL
# -----------------------------

def send_email(name,email,ctype):

    try:

        price=PRICING.get(ctype)

        body=f"""
Hello {name},

Thank you for submitting your {ctype} request.

Our editorial team is preparing your content.

Preview Access:
25% of the article will be visible for preview.

Content Plans:

Single Article: {price[0]}

10 Articles Monthly Plan: {price[1]}

15 Articles Monthly Plan: {price[2]}

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

        print("CLIENT EMAIL ERROR:",e)


# -----------------------------
# ADMIN NOTIFICATION EMAIL
# -----------------------------

def notify_admin(data):

    try:

        body=f"""

New Request Received

Name: {data['name']}
Email: {data['email']}
Content Type: {data['type']}
Topic: {data['topic']}
Audience: {data['audience']}
Keywords: {data['keywords']}
Brand: {data['brand']}
Website: {data['website']}

"""

        msg=MIMEText(body)

        msg["Subject"]="New ContentForge Request"
        msg["From"]=EMAIL_USER
        msg["To"]=ADMIN_EMAIL

        s=smtplib.SMTP("smtp.gmail.com",587)
        s.starttls()
        s.login(EMAIL_USER,EMAIL_PASS)
        s.send_message(msg)
        s.quit()

    except Exception as e:

        print("ADMIN EMAIL ERROR:",e)


# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# FORM SUBMISSION
# -----------------------------

@app.route("/submit",methods=["POST"])
def submit():

    try:

        data=request.get_json()

        conn=db()
        cur=conn.cursor()

        cur.execute("""

        INSERT INTO orders
        (name,email,content_type,topic,audience,keywords,brand,website,instructions)

        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)

        """,

        (

        data["name"],
        data["email"],
        data["type"],
        data["topic"],
        data["audience"],
        data["keywords"],
        data["brand"],
        data["website"],
        data["details"]

        )

        )

        conn.commit()

        cur.close()
        conn.close()

        send_email(data["name"],data["email"],data["type"])
        notify_admin(data)

        return jsonify({"success":True})

    except Exception as e:

        print("SERVER ERROR:",e)

        return jsonify({"error":"Server failure"}),500


# -----------------------------
# RUN SERVER
# -----------------------------

if __name__=="__main__":

    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
