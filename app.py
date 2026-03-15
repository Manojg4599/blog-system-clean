from flask import Flask, render_template, request, jsonify
import os
import psycopg2
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

DB_URL = os.getenv("DB_URL")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def get_connection():
    return psycopg2.connect(DB_URL)


def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id SERIAL PRIMARY KEY,
        customer_name TEXT,
        customer_email TEXT,
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


init_db()


@app.route("/")
def home():
    return render_template("index.html")


def send_email(to_email,name):

    subject="Your Content Planning Request Received"

    body=f"""
Hello {name},

Thank you for submitting your content request to ContentForge.

Our editorial planning team has received your request and will now review your requirements to prepare a structured content planning sheet tailored to your topic, audience, and SEO objectives.

Our process follows a professional editorial workflow used by leading content agencies:

Request Received
↓
Content Planning Sheet Prepared
↓
Editorial Review
↓
Human Written Content Development

This process ensures every article is structured strategically for readability, SEO performance, and audience engagement.

If additional clarification is required, our team may contact you before drafting begins.

Best regards,
ContentForge Editorial Team
"""

    msg=MIMEText(body)
    msg["Subject"]=subject
    msg["From"]=EMAIL_USER
    msg["To"]=to_email

    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(EMAIL_USER,EMAIL_PASS)
    server.send_message(msg)
    server.quit()


@app.route("/submit", methods=["POST"])
def submit():

    data=request.get_json()

    required=["name","email","type","topic","audience","length"]

    for field in required:

        if not data.get(field):

            return jsonify({
                "status":"error",
                "message":f"The field '{field}' is required."
            })

    try:

        conn=get_connection()
        cur=conn.cursor()

        cur.execute(
        """
        INSERT INTO orders
        (customer_name,customer_email,content_type,topic,audience,length,keywords,brand,instructions)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
        data.get("name"),
        data.get("email"),
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

        send_email(data.get("email"),data.get("name"))

        return jsonify({
        "status":"success",
        "message":"Your request has been submitted successfully. Please check your email."
        })

    except Exception as e:

        return jsonify({
        "status":"error",
        "message":"System error while saving request."
        })


@app.route("/keywords", methods=["POST"])
def keywords():

    data=request.get_json()

    topic=data.get("topic","").lower()

    if not topic:
        return jsonify({"keywords":[]})

    suggestions=[
    topic,
    f"best {topic}",
    f"{topic} guide",
    f"{topic} comparison",
    f"top {topic}",
    f"{topic} benefits",
    f"{topic} for beginners",
    f"how to choose {topic}",
    f"{topic} tools",
    f"{topic} alternatives"
    ]

    return jsonify({"keywords":suggestions})


if __name__=="__main__":

    port=int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=port)
