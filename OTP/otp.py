from flask import Flask, request, render_template, session, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from secrets import token_hex
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'jabernyarukalamaoidhogot'

# Email configuration 
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'oluochrachel384@gmail.com'
EMAIL_PASSWORD = 'iryu hpea qdol zony'

# In-memory OTP store (for simplicity, use a database in production)
otp_store = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        #Generate A six number otp
        otp = token_hex(3).upper()  
        otp_store[email] = {'otp': otp, 'expiry': datetime.utcnow() + timedelta(minutes=5)}
        
        # Send email with OTP
        try:
            msg = MIMEText(f'Your OTP is: {otp}')
            msg['Subject'] = 'Your OTP Code'
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = email
            
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
            
            flash('OTP sent to your email. Please check your inbox.', 'success')
        except Exception as e:
            flash(f'Failed to send email: {str(e)}', 'danger')
            return redirect(url_for('index'))
        
        return redirect(url_for('verify'))
    
    return render_template('index.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        email = request.form['email']
        entered_otp = request.form['otp']
        
        if email in otp_store:
            stored_otp = otp_store[email]['otp']
            expiry = otp_store[email]['expiry']
            
            if datetime.utcnow() > expiry:
                flash('OTP expired. Please request a new one.', 'danger')
                return redirect(url_for('index'))
            
            if entered_otp == stored_otp:
                flash('OTP verified successfully!', 'success')
                otp_store.pop(email)  # Clear OTP after successful verification
                return redirect(url_for('index'))
            else:
                flash('Incorrect OTP. Please try again.', 'danger')
        else:
            flash('No OTP request found for this email.', 'danger')
        
    return render_template('verify.html')

if __name__ == '__main__':
    app.run(debug=True)
