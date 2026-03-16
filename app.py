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


# ------------------------------
# CONTENT PRICING TABLE
# ------------------------------

PRICING = {

"Blog Article": {
"single":"₹1,050",
"plan10":"₹8,500 / month (10 Articles)",
"plan15":"₹12,000 / month (15 Articles)"
},

"SEO Landing Page": {
"single":"₹1,250",
"plan10":"₹10,000 / month (10 Pages)",
"plan15":"₹14,000 / month (15 Pages)"
},

"Comparison Page": {
"single":"₹1,150",
"plan10":"₹9,200 / month (10 Articles)",
"plan15":"₹13,000 / month (15 Articles)"
},

"Educational Guide": {
"single":"₹1,350",
"plan10":"₹10,800 / month (10 Guides)",
"plan15":"₹15,000 / month (15 Guides)"
},

"FAQ Page": {
"single":"₹900",
"plan10":"₹7,200 / month (10 Pages)",
"plan15":"₹10,000 / month (15 Pages)"
},

"Tool Page": {
"single":"₹1,200",
"plan10":"₹9,500 / month (10 Pages)",
"plan15":"₹13,500 / month (15 Pages)"
},

"Directory Page": {
"single":"₹1,100",
"plan10":"₹8,800 / month (10 Pages)",
"plan15":"₹12,500 / month (15 Pages)"
},

"Speech": {
"single":"₹1,500",
"plan10":"₹12,000 / month (10 Speeches)",
"plan15":"₹17,000 / month (15 Speeches)"
},

"Essay": {
"single":"₹900",
"plan10":"₹7,000 / month (10 Essays)",
"plan15":"₹9,500 / month (15 Essays)"
},

"Official Letter": {
"single":"₹700",
"plan10":"₹5,500 / month (10 Letters)",
"plan15":"₹7,500 / month (15 Letters)"
}

}


# ------------------------------
# DATABASE INIT
# ------------------------------

def init_db():

    conn=get_connection()
    cur=conn.cursor()

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


# ------------------------------
# HOME PAGE
# ------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ------------------------------
# SEND EMAIL FUNCTION
# ------------------------------

def send_email(to_email,name,content_type):

    price = PRICING.get(content_type)

    body=f"""
Hello {name},

Thank you for submitting your {content_type} request.

Our editorial team has received your topic and will now begin preparing a fully SEO-optimised article tailored specifically to your subject and target audience.

At ContentForge, every article is prepared through a structured editorial process designed to produce content that is both search-optimized and reader-friendly.

------------------------------------------------------------

What Happens Next

1. Your request will first be reviewed by our editorial planner to understand the topic, audience, and SEO direction.

2. A fully SEO-optimised article will be prepared based on your topic.

3. The article will be shared with you within approximately 2 hours.

Preparing the article requires time because our team collects and integrates several components to ensure the final output is professionally structured and visually engaging.

This preparation includes:

• Featured image concepts
• Supporting diagrams and visual explanations
• Comparison tables where applicable
• SEO-optimized headings and content structure
• Structured data elements for improved search visibility
• Supporting examples and explanatory sections

All these elements are assembled together so that the article is ready for publishing and optimized for search performance.

------------------------------------------------------------

Article Preview Access

The article you receive will contain:

• Complete article structure
• Real SEO-optimised writing style
• Professional formatting with headings and sections

For new clients evaluating our service, 25% of the article will be visible for preview.

The remaining sections remain locked until a content subscription plan is activated.

------------------------------------------------------------

Content Delivery Package

Each order produces a professional package:

ContentForge_Order_1042

Article.docx
SEO_Package.txt
Visual_Content_Plan.txt
Repurposing_Ideas.txt

------------------------------------------------------------

Content Plans for {content_type}

Single Order
{price['single']}

Professional Plan
{price['plan10']}

Growth Plan
{price['plan15']}

------------------------------------------------------------

Once a subscription plan is activated, all articles are delivered fully unlocked along with the complete Content Delivery Package.

Your article is currently in the editorial preparation stage and will be shared with you shortly.

Best regards
ContentForge Editorial Team
"""

    msg=MIMEText(body)

    msg["Subject"]="Your ContentForge Request Has Been Received — Editorial Preparation in Progress"

    msg["From"]=EMAIL_USER

    msg["To"]=to_email

    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(EMAIL_USER,EMAIL_PASS)
    server.send_message(msg)
    server.quit()


# ------------------------------
# FORM SUBMISSION
# ------------------------------

@app.route("/submit",methods=["POST"])

def submit():

    data=request.get_json()

    name=data.get("name")
    email=data.get("email")
    content_type=data.get("type")

    conn=get_connection()
    cur=conn.cursor()

    cur.execute(
    """
    INSERT INTO orders
    (customer_name,customer_email,content_type,topic,audience,length,keywords,brand,instructions)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,
    (
    name,
    email,
    content_type,
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

    send_email(email,name,content_type)

    return jsonify({
    "status":"success",
    "message":"Request submitted successfully. Please check your email."
    })


# ------------------------------
# RUN SERVER
# ------------------------------

if __name__=="__main__":

    port=int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=port)
