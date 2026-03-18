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


# ----------------------------
# DATABASE CONNECTION
# ----------------------------

def db():
    return psycopg2.connect(DB_URL, sslmode="require")


# ----------------------------
# CREATE TABLE
# ----------------------------

def init_db():

    try:

        conn = db()
        cur = conn.cursor()

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

        print("DB INIT ERROR:", e)


init_db()


# ----------------------------
# SEND CLIENT EMAIL
# ----------------------------

def send_email(name,email,ctype):

    try:

        body = f"""
Hello {name},

Thank you for submitting your {ctype} request.

Our editorial team is preparing your content.

Preview Access
Only 25% of the article will be visible initially.

Best Regards
ContentForge Editorial Team
"""

        msg = MIMEText(body)

        msg["Subject"] = "ContentForge Request Received"
        msg["From"] = EMAIL_USER
        msg["To"] = email

        s = smtplib.SMTP("smtp.gmail.com",587)
        s.starttls()
        s.login(EMAIL_USER,EMAIL_PASS)
        s.send_message(msg)
        s.quit()

    except Exception as e:

        print("EMAIL ERROR:",e)


# ----------------------------
# ADMIN EMAIL
# ----------------------------

def notify_admin(data):

    try:

        body = f"""

New Request Received

Name: {data.get('name')}
Email: {data.get('email')}
Content Type: {data.get('type')}
Topic: {data.get('topic')}
Keywords: {data.get('keywords')}

"""

        msg = MIMEText(body)

        msg["Subject"] = "New ContentForge Request"
        msg["From"] = EMAIL_USER
        msg["To"] = ADMIN_EMAIL

        s = smtplib.SMTP("smtp.gmail.com",587)
        s.starttls()
        s.login(EMAIL_USER,EMAIL_PASS)
        s.send_message(msg)
        s.quit()

    except Exception as e:

        print("ADMIN EMAIL ERROR:",e)


# ----------------------------
# HOME PAGE
# ----------------------------

@app.route("/")
def home():

    return render_template("index.html")


# ----------------------------
# FORM SUBMISSION
# ----------------------------

@app.route("/submit", methods=["POST"])
def submit():

    try:

        # Accept JSON OR form data
        data = request.get_json(silent=True)

        if not data:
            data = request.form

        name = data.get("name")
        email = data.get("email")
        ctype = data.get("type")
        topic = data.get("topic")
        audience = data.get("audience")
        keywords = data.get("keywords")
        brand = data.get("brand")
        website = data.get("website")
        details = data.get("details")

        if not name or not email or not topic or not keywords:

            return jsonify({"error":"Required fields missing"}),400


        conn = db()
        cur = conn.cursor()

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
        notify_admin(data)

        return jsonify({"success":True})


    except Exception as e:

        print("SERVER ERROR:", e)

        return jsonify({"error":"Server failure"}),500


# ----------------------------
# RUN SERVER
# ----------------------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0", port=port)
