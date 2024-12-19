1. Import Statements
python
 
from flask import Flask, request, render_template, session, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from secrets import token_hex
from datetime import datetime, timedelta
Flask:
Flask: Creates the application instance.
request: Accesses form data sent by the user.
render_template: Renders HTML templates for the app.
session: Stores data (like the OTP) across user sessions securely.
redirect and url_for: Redirects the user to different pages dynamically.
flash: Sends messages to users for feedback, like success or error notifications.
smtplib: A Python library for sending emails via the SMTP protocol.
MIMEText: Creates the content (body) of the email in text format.
secrets.token_hex: Generates a secure random token for OTP.
datetime, timedelta: Used to manage and compare timestamps, particularly for OTP expiration.
2. Flask App Initialization
python
 
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key
app = Flask(__name__): Creates the Flask application object.
app.secret_key: Encrypts session data and prevents tampering. Replace it with a secure key, generated using methods like secrets.token_hex.
3. Email Configuration
python
 
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'your_email@example.com'  # Replace with your email
EMAIL_PASSWORD = 'your_email_password'  # Replace with your email password
SMTP_SERVER and SMTP_PORT: Define the server and port for Gmail SMTP.
EMAIL_ADDRESS: The email address that sends OTPs.
EMAIL_PASSWORD: The password for authentication (App Password for Gmail accounts with 2-Step Verification).
4. OTP Store
python
 
otp_store = {}
A dictionary to temporarily store OTPs with associated email addresses and expiry timestamps. This is for demonstration purposes. Use a database for production.
5. Route for OTP Request
python
 
@app.route('/', methods=['GET', 'POST'])
def index():
@app.route('/'): Defines the route for the homepage.
methods=['GET', 'POST']: Allows both GET (display form) and POST (handle form submission) requests.
Inside the index function:
python
 
if request.method == 'POST':
    email = request.form['email']
    otp = token_hex(3).upper()  # Generate a secure 6-character OTP
    otp_store[email] = {'otp': otp, 'expiry': datetime.utcnow() + timedelta(minutes=5)}
request.form['email']: Retrieves the email input from the form.
token_hex(3).upper(): Generates a 6-character secure random OTP.
otp_store[email]: Stores the OTP and its expiry time (5 minutes from now) in the dictionary.
Sending the Email
python
 
try:
    msg = MIMEText(f'Your OTP is: {otp}')
    msg['Subject'] = 'Your OTP Code'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
MIMEText: Prepares the email body with the OTP.
msg['Subject']: Sets the email's subject line.
msg['From'] and msg['To']: Specify the sender and recipient.
python
 
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()  # Starts a secure TLS connection
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Logs in to the SMTP server
    server.send_message(msg)  # Sends the email
smtplib.SMTP: Connects to the SMTP server.
server.starttls: Encrypts communication with the server using TLS.
server.login: Authenticates with the SMTP server using the provided credentials.
server.send_message: Sends the email.
Feedback to the User
python
 
flash('OTP sent to your email. Please check your inbox.', 'success')
return redirect(url_for('verify'))
flash: Sends a success message to the user.
redirect(url_for('verify')): Redirects the user to the OTP verification page.
6. Route for OTP Verification
python
 
@app.route('/verify', methods=['GET', 'POST'])
def verify():
@app.route('/verify'): Defines the route for the OTP verification page.
Inside the verify function:
python
 
if request.method == 'POST':
    email = request.form['email']
    entered_otp = request.form['otp']
request.form['email'] and request.form['otp']: Retrieve the email and OTP entered by the user.
python
 
if email in otp_store:
    stored_otp = otp_store[email]['otp']
    expiry = otp_store[email]['expiry']
email in otp_store: Checks if the email has an OTP stored.
stored_otp: Retrieves the OTP associated with the email.
expiry: Retrieves the OTP's expiration time.
Check Expiry and Match OTP
python
 
if datetime.utcnow() > expiry:
    flash('OTP expired. Please request a new one.', 'danger')
    return redirect(url_for('index'))
datetime.utcnow() > expiry: Checks if the OTP has expired.
flash: Displays an error message and redirects to request a new OTP.
python
 
if entered_otp == stored_otp:
    flash('OTP verified successfully!', 'success')
    otp_store.pop(email)  # Clear OTP after successful verification
    return redirect(url_for('index'))
entered_otp == stored_otp: Compares the entered OTP with the stored OTP.
otp_store.pop(email): Deletes the OTP entry after successful verification to prevent reuse.
python
 
flash('Incorrect OTP. Please try again.', 'danger')
Displays an error message if the OTP doesn't match.
7. Run the Flask App
python
 
if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__': Ensures the app runs only when executed directly, not imported.
app.run(debug=True): Runs the Flask development server with debug mode enabled for easier debugging.
Templates
The templates (index.html and verify.html) handle form rendering and user feedback. Flask dynamically injects messages (flash) and handles user input through forms.
