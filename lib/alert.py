# STD Modules
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Email configuration
# SENDER = 'cryptobot8485@gmail.com' # Sender
SENDER = os.environ.get('SENDER_MAIL')

# PASSWORD = 'otwx mqmy tuip ffly' # Sender's Password
PASSWORD = os.environ.get('SENDER_PASS')


# RECIVER = 'vaibhavumbarkar8485@gmail.com' # Receiver
RECEIVER = os.environ.get('RECEIVER_MAIL')



def send_alert(action, coin_name, current_price, m1, m2, r1, r2, p1, p2, s1, s2):
    message = f"""
    Crypto Bot :

    - Action : {action}
    - Coin Name : {coin_name}
    - Price : {current_price}
    

    Advance Information :

    - MACD Signal : {m1}
    - MACD Value (+/-) : {m2}

    - RSI Signal : {r1}
    - RSI Value (60/30) : {r2}

    - Price Percentage Oscillator : {p1}
    - Price Percentage Oscillator (+/-) : {p2}

    - Stochastic Oscillator : {s1}
    - Stochastic Oscillator (80/20) : {s2}

    (NOTE : Timeframe: 1w for above information)

    """

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = RECEIVER
    msg['Subject'] = 'Crypto Alert!'

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
        print(f'Crypto Bot: {action} Alert Send Successfully.')
    except Exception as e:
        print(f'Failed to send Alert. Error: {str(e)}')
