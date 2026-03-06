from flask import Flask, render_template_string, request
from email_sender import send_email
import os

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Email Dashboard</title>
</head>
<body>
    <h2>Email Automation Dashboard</h2>
    <form method="POST">
        <label>Recipient Email:</label><br>
        <input type="email" name="recipient" required><br><br>

        <label>Subject:</label><br>
        <input type="text" name="subject" required><br><br>

        <label>Message:</label><br>
        <textarea name="message" rows="5" required></textarea><br><br>

        <button type="submit">Send Email</button>
    </form>
    <p>{{ result }}</p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        recipient = request.form["recipient"]
        subject = request.form["subject"]
        message = request.form["message"]

        success = send_email(recipient, subject, message)

        if success:
            result = "Email Sent Successfully!"
        else:
            result = "Failed to Send Email."

    return render_template_string(HTML_FORM, result=result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
