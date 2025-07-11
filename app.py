import os
import logging
from flask import redirect
from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from flask_mail import Mail, Message

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)


@app.route('/')
def index():
    """Main portfolio page"""
    return render_template('index.html')


@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submission"""
    try:
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validate form data
        if not all([name, email, subject, message]):
            flash('All fields are required.', 'error')
            return redirect(url_for('index') + '#contact')
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('index') + '#contact')
        
        # Send email if mail is configured
        if app.config.get('MAIL_USERNAME'):
            try:
                msg = Message(
                    subject=f'Portfolio Contact: {subject}',
                    recipients=[app.config['MAIL_USERNAME']],
                    body=f'''
Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
                    ''',
                    reply_to=email
                )
                mail.send(msg)
                flash('Thank you for your message! I will get back to you soon.', 'success')
            except Exception as e:
                logging.error(f"Failed to send email: {str(e)}")
                flash('Message received! However, there was an issue sending the email notification.', 'warning')
        else:
            # Log the message if mail is not configured
            logging.info(f"Contact form submission - Name: {name}, Email: {email}, Subject: {subject}, Message: {message}")
            flash('Thank you for your message! I will get back to you soon.', 'success')
        
    except Exception as e:
        logging.error(f"Error processing contact form: {str(e)}")
        flash('An error occurred while processing your message. Please try again.', 'error')
    
    return redirect(url_for('index') + '#contact')




@app.route('/resume', endpoint='resume')
def download_resume():
    """Redirect to Google Drive resume download link"""
    drive_link = "https://drive.google.com/uc?export=download&id=14Q-KRTnNKvcqvpgd8i9NJifK50QqMSAk"
    return redirect(drive_link)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

