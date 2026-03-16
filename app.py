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


PRICING = {

"Blog Article":("₹1,050","₹8,500 / month (10)","₹12,000 / month (15)"),
"SEO Landing Page":("₹1,250","₹10,000 / month (10)","₹14,000 / month (15)"),
"Comparison Article":("₹1,150","₹9,200 / month (10)","₹13,000 / month (15)"),
"Educational Guide":("₹1,350","₹10,800 / month (10)","₹15,000 / month (15)"),
"FAQ Page":("₹900","₹7,200 / month (10)","₹10,000 / month (15)"),
"Tool Page":("₹1,200","₹9,500 / month (10)","₹13,500 / month (15)"),
"Directory Page":("₹1,100","₹8,800 / month (10)","₹12,500 / month (15)"),
"Speech":("₹1,500","₹12,000 / month (10)","₹17,000 / month (15)"),
"Essay":("₹900","₹7,000 / month (10)","₹9,500 / month (15)"),
"Official Letter":("₹700","₹5,500 / month (10)","₹7,500 / month (15)")

}


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


def send_client_email(name,email,content_type):

    price=PRICING.get(content_type)

    body=f"""

Hello {name},

Thank you for submitting your {content_type} request.

Our editorial team will now prepare a fully SEO optimised article based on your topic.

The article will be delivered within approximately 2 hours.

Preview Access
25% of the article will be visible so that you can evaluate writing quality.

Remaining sections unlock once a subscription plan is activated.

Content Delivery Package

Article.docx
SEO_Package.txt
Visual_Content_Plan.txt
Repurposing_Ideas.txt


Content Plans

Single Article
{price[0]}

Professional Plan
{price[1]}

Growth Plan
{price[2]}

Best Regards
ContentForge Editorial Team

"""

    msg=MIMEText(body)

    msg["Subject"]="ContentForge Request Received"
    msg["From"]=EMAIL_USER
    msg["To"]=email

    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(EMAIL_USER,EMAIL_PASS)
    server.send_message(msg)
    server.quit()


def send_admin_email(data):

    website_link = data["website"]

    if website_link:
        website_display=f"<a href='{website_link}'>{website_link}</a>"
    else:
        website_display="Not Provided"

    body=f"""

New Content Request

Name: {data['name']}
Email: {data['email']}
Content Type: {data['type']}
Topic: {data['topic']}
Audience: {data['audience']}
Keywords: {data['keywords']}
Brand: {data['brand']}
Website: {website_display}

"""

    msg=MIMEText(body,"html")

    msg["Subject"]="New ContentForge Request"
    msg["From"]=EMAIL_USER
    msg["To"]=ADMIN_EMAIL

    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(EMAIL_USER,EMAIL_PASS)
    server.send_message(msg)
    server.quit()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit",methods=["POST"])
def submit():

    data=request.get_json()

    required=["name","email","topic","keywords"]

    for r in required:
        if not data.get(r):
            return jsonify({"error":f"{r} is required"})


    conn=get_connection()
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

    send_client_email(data["name"],data["email"],data["type"])
    send_admin_email(data)

    return jsonify({"success":True})


if __name__=="__main__":

    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
