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


def db():
    return psycopg2.connect(DB_URL)


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

    price=PRICING.get(ctype)

    body=f"""
Hello {name},

Thank you for submitting your {ctype} request.

Our editorial team has received your topic and will now begin preparing a fully SEO-optimised article tailored specifically to your subject and target audience.

What Happens Next

1. Your request will be reviewed by our editorial planner.
2. A fully SEO-optimised article will be prepared.
3. The article will be shared within approximately 2 hours.

Article Preview Access

25% of the article will be visible for preview.
Remaining sections unlock once a subscription plan is activated.

Content Delivery Package

Article.docx
SEO_Package.txt
Visual_Content_Plan.txt
Repurposing_Ideas.txt

Content Plans

Single Order: {price[0]}

Professional Plan: {price[1]}

Growth Plan: {price[2]}

Best Regards
ContentForge Editorial Team
"""

    msg=MIMEText(body)

    msg["Subject"]="Your ContentForge Request Has Been Received"
    msg["From"]=EMAIL_USER
    msg["To"]=email

    s=smtplib.SMTP("smtp.gmail.com",587)
    s.starttls()
    s.login(EMAIL_USER,EMAIL_PASS)
    s.send_message(msg)
    s.quit()


def notify_admin(data):

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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit",methods=["POST"])
def submit():

    data=request.get_json()

    if not data["name"]:
        return jsonify({"error":"Name required"})

    if not data["email"]:
        return jsonify({"error":"Email required"})

    if not data["topic"]:
        return jsonify({"error":"Topic required"})

    if not data["keywords"]:
        return jsonify({"error":"SEO Keywords required"})


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


if __name__=="__main__":

    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
