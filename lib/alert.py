# STD Modules
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
SENDER = os.environ.get('SENDER_MAIL')
PASSWORD = os.environ.get('SENDER_PASS')
RECEIVER = os.environ.get('RECEIVER_MAIL')

# Validate environment variables
if not SENDER or not PASSWORD or not RECEIVER:
    raise ValueError("Please set the environment variables for email configuration.")

# Main Function
def send_email(subject, message):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = RECEIVER
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to gmail's SMTP server using SSL
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER, PASSWORD)
        
        # Send the email
        server.sendmail(SENDER, RECEIVER, msg.as_string())
        
        # Close the connection
        server.quit()
        print('Gmail send.')

    except Exception as e:
        error_message = f'Failed to send email. Error: {str(e)}'
        print(error_message)
        
        # Optionally, send an email to the sender about the error
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, SENDER, f"Subject: Gmail Sending Failed\n\n{error_message}")
            server.quit()
        except Exception as inner_e:
            print(f'Failed to notify sender about the gmail error. Error: {str(inner_e)}')

def send_alert(msg):
    message = f"Message : {msg}"
    send_email('Alert!', message)

# Order Notification Function
def send_order_alert(side, response):
    message = f"""
        Action: {side}
        Symbol: {response['data']['symbol']}
        Price: {response['data']['price']}
        Quantity: {response['data']['executed_qty']}
        """
    send_email('Crypto Order Placed', message)
