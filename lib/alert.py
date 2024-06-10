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

def send_order_alert(response):
    message = f"*Message : {response}"
    send_email('Crypto Order', message)

def send_notification_alert(action, coin, price, signal_1d, signal_1w, s1, s2, s3, s4, h1_1d, h2_1d, h1_1w, h2_1w, error):
    if action == 'Buy':
        message = f"""
        - Order Action: {action}
        - Coin Name: {coin}
        - Current Price: {price}

        
        Details:
        
        Daily Chart Signal: {signal_1d}
          - All Indicators: [ Buy: {s1}, Hold: {h1_1d} ] / 44
          - Imp Indicators: [ Buy: {s2}, Hold: {h2_1d} ] / 21
        Weekly Chart Signal: {signal_1w}
          - All Indicators: [ Buy: {s3}, Hold: {h1_1w} ] / 44
          - Imp Indicators: [ Buy: {s4}, Hold: {h2_1w} ] / 21

        *Message : [{error}]     
        """
    else:
        message = f"""
        - Order Action: {action}
        - Coin Name: {coin}
        - Current Price: {price}

        
        Details:
        
        Daily Chart Signal: {signal_1d}
          - All Indicators: [ Sell: {s1}, Hold: {h1_1d} ] / 44
          - Imp Indicators: [ Sell: {s2}, Hold: {h2_1d} ] / 21
        Weekly Chart Signal: {signal_1w}
          - All Indicators: [ Sell: {s3}, Hold: {h1_1w} ] / 44
          - Imp Indicators: [ Sell: {s4}, Hold: {h2_1w} ] / 21

        *Message : [{error}]  
        """
    send_email('Crypto Alert', message)
