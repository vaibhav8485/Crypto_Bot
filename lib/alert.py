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

# Order Notification Function
def send_order_alert(response):
    message = f"*Message : {response}"
    send_email('Crypto Order', message)

# Alert Notification Function
def send_notification_alert(action, coin, price, signal_1d, signal_1w, momentum_buy, trend_buy, volatility_buy, volume_buy, momentum_sell, trend_sell, volatility_sell, volume_sell, error):
    if action == 'Buy':
        message = f"""
        Order Action: {action}
        Coin Name: {coin}
        Current Price: {price}

        
        [[DETAILS]]
        
        Daily Timeframe Signal: {signal_1d}
        Weekly Timeframe Signal: {signal_1w}

        Momentum: {momentum_buy}/11
        Trend: {trend_buy}/6
        Volatility: {volatility_buy}/8
        Volume: {volume_buy}/6

        *MESSAGE: [{error}]     
        """
    else:
        message = f"""
        Order Action: {action}
        Coin Name: {coin}
        Current Price: {price}

        
        [[DETAILS]]
        
        Daily Timeframe Signal: {signal_1d}
        Weekly Timeframe Signal: {signal_1w}

        Momentum: {momentum_sell}/11
        Trend: {trend_sell}/6
        Volatility: {volatility_sell}/8
        Volume: {volume_sell}/6
        
        *MESSAGE: [{error}]  
        """
    send_email('Crypto Alert', message)
