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


def get_connection():
    return psycopg2.connect(DB_URL)


# ----------------------
# PRICING TABLE
# ----------------------

PRICING = {

"Blog Article":{
"single":"₹1,050",
"plan10":"₹8,500 / month (10 Articles)",
"plan15":"₹12,000 / month (15 Articles)"
},

"SEO Landing Page":{
"single":"₹1,250",
"plan10":"₹10,000 / month (10 Pages)",
"plan15":"₹14,000 / month (15 Pages)"
},

"Comparison Page":{
"single":"₹1,150",
"plan10":"₹9,200 / month (10 Articles)",
"plan15":"₹13,000 / month (15 Articles)"
},

"Educational Guide":{
"single":"₹1,350",
"plan10":"₹10,800 / month (10 Guides)",
"plan15":"₹15,000 / month (15 Guides)"
},

"FAQ Page":{
"single":"₹900",
"plan10":"₹7,200 / month (10 Pages)",
"plan15":"₹10,000 / month (15 Pages)"
}

}


# ----------------------
# DATABASE INIT
# ----------------------

def init_db():

    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""

    CREATE TABLE IF NOT EXISTS orders(

    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    content_type TEXT,
    topic TEXT,
    audience TEXT,
    length TEXT,
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


# ----------------------
# EMAIL FUNCTION
# ----------------------

def send_email(to_email,name,content_type):

    price = PRICING.get(content_type)

    body=f"""
Hello {name},

Thank you for submitting your {content_type} request.

Our editorial team will now prepare a fully SEO optimised article based on your topic.

The article will be delivered within approximately 2 hours.

Content Preview
You will receive an article preview where 25% of the article will be visible.

The remaining content will unlock once a subscription plan is activated.

Content Delivery Package

Article.docx
SEO_Package.txt
Visual_Content_Plan.txt
Repurposing_Ideas.txt


Content Plans

Single Article
{price['single']}

Professional Plan
{price['plan10']}

Growth Plan
{price['plan15']}

Best Regards
ContentForge Editorial Team
"""

    msg=MIMEText(body)

    msg["Subject"]="ContentForge Request Received"

    msg["From"]=EMAIL_USER
    msg["To"]=to_email

    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(EMAIL_USER,EMAIL_PASS)
    server.send_message(msg)
    server.quit()


# ----------------------
# ADMIN EMAIL
# ----------------------

def notify_admin(data):

    body=f"""
NEW CONTENT REQUEST

Name: {data['name']}
Email: {data['email']}
Content Type: {data['type']}
Topic: {data['topic']}
Audience: {data['audience']}
Brand: {data['brand']}
Website: {data['website']}

Please login to review.
"""

    msg=MIMEText(body)

    msg["Subject"]="New ContentForge Request"
    msg["From"]=EMAIL_USER
    msg["To"]=ADMIN_EMAIL

    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(EMAIL_USER,EMAIL_PASS)
    server.send_message(msg)
    server.quit()


# ----------------------
# HOME PAGE
# ----------------------

@app.route("/")
def home():
    return render_template("index.html")


# ----------------------
# FORM SUBMIT
# ----------------------

@app.route("/submit",methods=["POST"])

def submit():

    data=request.get_json()

    if not data["name"]:
        return jsonify({"error":"Please enter your name"})

    if not data["email"]:
        return jsonify({"error":"Please enter your email"})


    conn=get_connection()
    cur=conn.cursor()

    cur.execute(
    """

    INSERT INTO orders
    (name,email,content_type,topic,audience,length,keywords,brand,website,instructions)

    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

    """,

    (

    data["name"],
    data["email"],
    data["type"],
    data["topic"],
    data["audience"],
    data["length"],
    data["keywords"],
    data["brand"],
    data["website"],
    data["details"]

    )

    )

    conn.commit()
    cur.close()
    conn.close()

    send_email(data["email"],data["name"],data["type"])
    notify_admin(data)

    return jsonify({"success":True})


if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
