from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your email provider's SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')  # Store email in environment variables
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')  # Store password securely
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER')

mail = Mail(app)

app.secret_key = 'supersecretkey'  # Needed for flash messages

# Route for Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Route for About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for Skills Page
@app.route('/skills')
def skills():
    return render_template('skills.html')

# Route for Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Create the email message
        msg = Message("New Contact Form Submission",
                      sender=email,
                      recipients=[os.environ.get('EMAIL_USER')])  # Your email to receive messages
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        try:
            mail.send(msg)
            # Instead of flash, we'll return a success message for JavaScript to handle
            return "Message sent successfully!"  # Return a simple success string
        except Exception as e:
            # Return an error message for JavaScript to handle
            return f"Error sending message. Please try again. Error: {e}"  # Return the error

    return render_template('contact.html')

# Route for Projects Page
@app.route('/projects')
def projects():
    return render_template('projects.html')

if __name__ == '__main__':
    app.run(debug=True)