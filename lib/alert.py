# STD Modules
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
SENDER = os.environ.get('SENDER_MAIL')
PASSWORD = os.environ.get('SENDER_PASS')
RECEIVER = os.environ.get('RECEIVER_MAIL')

def send_alert(action, coin, price):
    message = f"""
    Crypto Bot :
    - Order Action : {action}
    - Coin Name : {coin}
    - Current Price : {price}
    
    Details :
    - Daily Chart Analysis : 
    - Weekly Chart Analysis :
    """
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = RECEIVER
    msg['Subject'] = f'{coin} {action} Alert'

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER, PASSWORD)
        
        # Send the email
        server.sendmail(SENDER, RECEIVER, msg.as_string())
        
        # Close the connection
        server.quit()
        print(f'{coin_name} {action} Alert Send Successfully.')

    except Exception as e:
        print(f'Failed to send Alert. Error: {str(e)}')
