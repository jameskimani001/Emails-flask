import os
import re  # Import the re module for regex
from flask import Flask, request, render_template_string
from flask_mail import Mail, Message
from flask_migrate import Migrate
from models import db, User, Todo, Tag

app = Flask(__name__)

# Secure Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Replace with environment variable
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Replace with environment variable
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')  # Same as the sender email

mail = Mail(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mail.db'

# Initialize the db and migrate
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/send-email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        recipient = request.form.get('email')
        subject = request.form.get('subject')
        body = request.form.get('body')

        if not is_valid_email(recipient):
            return "Invalid email format."

        # Create and send message
        msg = Message(subject=subject, recipients=[recipient], body=body)
        try:
            mail.send(msg)
            return f"Email sent to {recipient}!"
        except Exception as e:
            return f"Failed to send email. Error: {str(e)}"

    return render_template_string('''
        <form method="POST" style="width: 300px; margin: 0 auto;">
            <label for="email">Email:</label>
            <input type="email" name="email" required><br><br>

            <label for="subject">Subject:</label>
            <input type="text" name="subject" required><br><br>

            <label for="body">Body:</label>
            <textarea name="body" required></textarea><br><br>

            <button type="submit">Send Email</button>
        </form>
    ''')

def is_valid_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email) is not None

if __name__ == '__main__':
    app.run(debug=True)
