from flask import Flask, request, render_template_string
from flask_mail import Mail, Message
from flask_migrate import Migrate  # Corrected import
from models import db, User, Todo, Tag  # Import db from models.py

app = Flask(__name__)

# Configure Flask-Mail with Gmail SMTP
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # TLS port
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Replace with your Gmail email
app.config['MAIL_PASSWORD'] = 'xlmkweqntqovusqx'  # Use the 16-character app password
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'  # Replace with your Gmail

mail = Mail(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mail.db'

# Initialize the db and migrate
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/send-email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        recipient = request.form.get('email')  # Get the email from form
        subject = request.form.get('subject')  # Get the subject from form
        body = request.form.get('body')  # Get the body from form

        # Create a message object
        msg = Message(subject=subject,
                      recipients=[recipient],
                      body=body)

        try:
            # Send the email
            mail.send(msg)
            return f"Email sent to {recipient}!"
        except Exception as e:
            return f"Failed to send email. Error: {str(e)}"

    return render_template_string('''
        <form method="POST">
            Email: <input type="email" name="email" required><br>
            Subject: <input type="text" name="subject" required><br>
            Body: <textarea name="body" required></textarea><br>
            <button type="submit">Send Email</button>
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
